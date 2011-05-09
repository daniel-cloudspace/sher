from django.db import models
from django.conf import settings
from os.path import join

UPLOAD_PATH = join(settings.MEDIA_ROOT, "%s")

#youtube valid categories, grabbed from http://gdata.youtube.com/schemas/2007/categories.cat
categories = {'Animals': 'Pets & Animals',
 'Autos': 'Autos & Vehicles',
 'Comedy': 'Comedy',
 'Education': 'Education',
 'Entertainment': 'Entertainment',
 'Film': 'Film & Animation',
 'Games': 'Gaming',
 'Howto': 'Howto & Style',
 'Movies': 'Movies',
 'Movies_Action_adventure': 'Movies - Action/Adventure',
 'Movies_Anime_animation': 'Movies - Anime/Animation',
 'Movies_Classics': 'Movies - Classics',
 'Movies_Comedy': 'Movies - Comedy',
 'Movies_Documentary': 'Movies - Documentary',
 'Movies_Drama': 'Movies - Drama',
 'Movies_Family': 'Movies - Family',
 'Movies_Foreign': 'Movies - Foreign',
 'Movies_Horror': 'Movies - Horror',
 'Movies_Sci_fi_fantasy': 'Movies - Sci-Fi/Fantasy',
 'Movies_Shorts': 'Movies - Shorts',
 'Movies_Thriller': 'Movies - Thriller',
 'Music': 'Music',
 'News': 'News & Politics',
 'Nonprofit': 'Nonprofits & Activism',
 'People': 'People & Blogs',
 'Shortmov': 'Short Movies',
 'Shows': 'Shows',
 'Sports': 'Sports',
 'Tech': 'Science & Technology',
 'Trailers': 'Trailers',
 'Travel': 'Travel & Events',
 'Videoblog': 'Videoblogging'}

category_choices = tuple([(k,v) for k,v in categories.items()])

#status_choices = ()

class Status(models.Model):
    """
    What Twitter made famous. Short messages, <160 characters, and
    meant to be sent out over such networks.
    """
    share_time = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=160)
    is_published = models.BooleanField(editable=False, default=0)

    services = models.ManyToManyField('Service')

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['share_time']
        verbose_name_plural = "Statuses"

class Image(models.Model):
    """
    An image to post to a gallery somewhere.
    """
    share_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=UPLOAD_PATH % "images")
    description = models.TextField(help_text="The description of the photo.", blank=True)
    tags = models.CharField(max_length=255,help_text="Space-delimited list of tags. Tags that contain spaces need to be quoted. Ex. \"central station\" ", blank=True)
    is_public = models.BooleanField(default=1, help_text="True if photo is public, false if it is private. Default is public.")
    is_published = models.BooleanField(editable=False, default=0)
    
    services = models.ManyToManyField('Service')

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['share_time']

class Post(models.Model):
    """
    A block of text > 160 characters. Pushed out to blog posts,
    Facebook Notes, etc.
    """
    share_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(blank=True, null=True)
    text = models.TextField()
    is_published = models.BooleanField(editable=False, default=0)
    
    services = models.ManyToManyField('Service')

    def __unicode__(self):
        return self.subject

    class Meta:
        ordering = ['share_time']

# TODO: Find video plugin for Django? django-video or django-videologue, maybe?
# https://github.com/andrewebdev/django-video
# Not sure which of the following would be preferred.
# http://hg.antonoff.info/tvon/django-videologue-html5/overview
# http://hg.antonoff.info/eternicode/django-videologue-html5/overview
#
# If we can't find anything fitting, mplayer -identify or something?
# We should verify length/size/format limits for the services, if so.
class Video(models.Model):
    """
    What it says on the tin.
    Push out to Flickr, YouTube, etc.
    """
    share_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=category_choices, help_text="Single cateogry this video belongs to.")
    description = models.TextField(blank=True, help_text="Short video description.")
    keywords = models.CharField(max_length=250, blank=True, help_text="Keywords seperated by comma.")
    video = models.FileField(upload_to = UPLOAD_PATH % "videos")
    is_published = models.BooleanField(editable=False, default=0)
    
    services = models.ManyToManyField('Service')

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['share_time']

class Service(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Service name. i.e youtube")
    account = models.ForeignKey('Account', help_text="The account you want to post as.")
    
    def __unicode__(self):
        return "Service: %s | Account: %s"  % ( self.name, self.account.user)

    @models.permalink
    def get_authorize_url(self):
        return ("%s-authorize" % self.name.lower(),)

class Account(models.Model):
    user = models.CharField(max_length=255, blank=True)
    oauth_token = models.CharField(max_length=255, blank=True)
    oauth_secret = models.CharField(max_length=255, blank=True)
    authsub_token = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return "Account: %s"  % (self.user,)
