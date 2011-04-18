import oauth2 as oauth
import sher.settings as settings
import cgi
import urlparse
import gdata.youtube
import gdata.youtube.service

class TwitterService(object):
    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
        self.client = oauth.Client(self.consumer)        

    def get_request_token(self):
        request_token_url = settings.TWITTER_REQUEST_TOKEN_URL
        resp, content = self.client.request(request_token_url, "POST")

        if resp['status'] != '200': 
            raise Exception("Invalid Response from Twitter")

        request_token = dict(cgi.parse_qsl(content))
        self.request_token = request_token['oauth_token']
        self.request_token_secret = request_token['oauth_token_secret']

        return self.request_token

    def get_access_token(self, oauth_verifier):
        access_token_url = settings.TWITTER_ACCESS_TOKEN_URL
        
        token = oauth.Token(self.request_token, self.request_token_secret)
        token.set_verifier(oauth_verifier)

        client = oauth.Client(self.consumer, token)
        
        resp, content = client.request(access_token_url, "POST")
        
        if resp['status'] != '200':
            raise Exception("Invalid Response from Twitter")

        access_token = dict(cgi.parse_qsl(content))
        self.access_token = access_token['oauth_token']
        self.access_token_secret = access_token['oauth_token_secret']

        return access_token
twitter_service = TwitterService(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)

class YouTubeService(object):
    def __init__(self, developer_key, client_id):
        self.developer_key = developer_key
        self.client_id = client_id
        self.yt_service = gdata.youtube.service.YouTubeService()
   
    def get_authsub_url(self, callback):
        next = callback
        scope = "http://gdata.youtube.com"
        secure = False
        session = True

        return self.yt_service.GenerateAuthSubURL(next, scope, secure, session)

    def upgrade_to_session(self, token):
        """
        Takes an authsub token and upgrades to session token then returns that token for storing.
        """
        self.yt_service.SetAuthSubToken(token)
        self.yt_service.UpgradeToSessionToken()

        return self.yt_service.GetAuthSubToken()
                
youtube_service = YouTubeService(settings.YOUTUBE_DEVELOPER_KEY, settings.YOUTUBE_CLIENT_ID)

class FacebookService(object):
    def __init__(self, app_id, app_key, app_secret):
        self.app_id = app_id
        self.app_key = app_key
        self.app_secret = app_secret
    
    def get_oauth_url(self):
        return "https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&scope=read_stream,publish_stream,offline_access"


    def get_access_token_url(self, callback, code):
        self.access_token_url = "https://graph.facebook.com/oauth/access_token?client_id=%s&redirect_uri=%s&client_secret=%s&code=%s" % (self.app_id, callback, self.app_secret, code)
        return self.access_token_url
    

facebook_service = FacebookService(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_KEY, settings.FACEBOOK_APP_SECRET)
