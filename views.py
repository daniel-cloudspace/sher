from django.http import HttpResponseRedirect, HttpResponse, Http404
from sher.models import Account, Service
from django.shortcuts import render
import sher.settings as settings
from sher.services import twitter_service, youtube_service, facebook_service, flickr_service
from django.contrib import messages
from django.core.urlresolvers import reverse
import urllib
import urllib2
import re

#TODO: Get rid of all hardcoded urls and put them in settings.

def index(request, template="sher/index.html"):
    """
    Serves as a listing for supported services and a way to authorize the _current_
    application with them.
    """
    return render(request, template, {'services': Service.objects.all()})

def authorize_twitter(request):
    """
    Handles getting the request token from the twitter API, redirects user to a page
    that requires user interaction to allow access to Twitter.
    """
    request_token = twitter_service.get_request_token()
    oauth_url = "%s?oauth_token=%s" % (settings.TWITTER_AUTHORIZE_URL, request_token)
    return HttpResponseRedirect(oauth_url)

def twitter_callback(request):
    """
    Handles the Twitter callback and gets the access_token then saves 
    it to an accounts database for future use.
    NOTE: Callback url is supplied in the twitter app settings.
    """

    oauth_verifier = request.GET['oauth_verifier']
    access_token = twitter_service.get_access_token(oauth_verifier)
    
    sobj, c = Service.objects.get_or_create(name__iexact="twitter")
    try:
        Account.objects.get(oauth_token=access_token['oauth_token'], service=sobj)
    except Account.DoesNotExist:
        account = Account()
        account.user = access_token['screen_name']
        account.oauth_token = access_token['oauth_token']
        account.oauth_secret = access_token['oauth_token_secret']
        account.service = sobj
        account.save()

    messages.success(request, "App authorized with Twitter.")
    return HttpResponseRedirect(reverse("sher-index"))


def authorize_youtube(request):
    """
    Redirects user to the youtube AuthSub url prompting or authorization then 
    redirects back to callback.
    """
    callback = "http://udderweb.com:8200/sher/youtube/callback/"
    return HttpResponseRedirect(youtube_service.get_authsub_url(callback))
    
def youtube_callback(request):
    """
    The youtube API will return with an authsub token this gets upgraded to a 
    session token and stored for future use.
    """
    token = request.GET['token']
    if not token: raise Exception("Youtube didn't return a token.")
    
    upgraded_token = youtube_service.upgrade_to_session(token)

    current_user = settings.YOUTUBE_USERNAME
    
    sobj, c = Service.objects.get_or_create(name__iexact="youtube")
    try:
        Account.objects.get(authsub_token=upgraded_token, service=sobj)
    except Account.DoesNotExist:
        account = Account()
        account.authsub_token = upgraded_token
        account.user = current_user
        account.service = sobj
        account.save()
    
    messages.success(request, "App authorized with YouTube")
    return HttpResponseRedirect(reverse("sher-index"))

def authorize_facebook(request):
    """
    Facebooks api will return a server generated code which we then hand off to the callback.
    """
    callback = "http://udderweb.com:8200/sher/facebook/callback/"
    oauth_url = facebook_service.get_oauth_url() % (facebook_service.app_id, urllib.quote(callback))
    return HttpResponseRedirect(oauth_url) 

def facebook_callback(request):
    """
    Has two purposes. The first is to receive the facebook server generated code and then query
    facebooks api for the actual access_token, grab that token and save an account.
    """
    
    if ('error_response' or 'error') in request.GET:
        raise Exception((request.GET['error_response'] or request.GET['error']))

    code = request.GET.get('code', '')

    if code:
        #in the presence of code we open up the access token url and get the access_token
        callback = "http://udderweb.com:8200/sher/facebook/callback/"
        access_token_url = facebook_service.get_access_token_url(callback, code) 
        access_token = urllib2.urlopen(access_token_url).read().split('access_token=')[1]       
        
        sobj, c = Service.objects.get_or_create(name__iexact="facebook")
        try:
            Account.objects.get(oauth_token=access_token, service=sobj)
        except Account.DoesNotExist:
            account = Account()
            account.user = settings.FACEBOOK_USER
            account.oauth_token = access_token
            account.service = sobj
            account.save()

    messages.success(request, "App authorized with Facebook")
    return HttpResponseRedirect(reverse("sher-index"))

def flickr_authorize(request):
    url = flickr_service.get_oauth_url()
    return HttpResponseRedirect(url)

def flickr_callback(request):
    if 'frob' in request.GET:
        frob = request.GET['frob']
        auth_token_url = flickr_service.get_auth_token(frob)
        data = urllib2.urlopen(auth_token_url).read()
        auth_token = re.search('<token>(.*)</token>', data).groups()[0]
       

        sobj, c = Service.objects.get_or_create(name__iexact="flickr")
        try:
            Account.objects.get(oauth_token=auth_token, service=sobj)
        except Account.DoesNotExist:
            account = Account()
            account.user = "tsoporan"
            account.oauth_token = auth_token
            account.service = sobj
            account.save()

    messages.success(request, "App authorized with Flickr")
    return HttpResponseRedirect(reverse("sher-index"))


