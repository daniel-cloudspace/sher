from django.conf.urls.defaults import patterns, include, url

from sher.views import index, authorize_twitter, twitter_callback, authorize_youtube, youtube_callback, authorize_facebook, facebook_callback, flickr_authorize, flickr_callback

urlpatterns = patterns('', 
    url(r'^$', index, name="sher-index"), 
    url(r'^twitter/authorize/$', authorize_twitter, name="twitter-authorize"),
    url(r'^twitter/callback/$', twitter_callback, name="twitter-callback"),
    url(r'^youtube/authorize/$', authorize_youtube, name="youtube-authorize"),
    url(r'^youtube/callback/$', youtube_callback, name="youtube-callback"),
    url(r'^facebook/authorize/$', authorize_facebook, name="facebook-authorize"),
    url(r'^facebook/callback/$', facebook_callback, name="facebook-callback"),
    url(r'^flickr/authorize/$', flickr_authorize, name="flickr-authorize"), 
    url(r'^flickr/callback/$',  flickr_callback, name="flickr-callbacl"),
)
