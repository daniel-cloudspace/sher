from django.db import models
from django.conf import settings
from os.path import join
import datetime

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
 #'Movies': 'Movies',
 #'Movies_Action_adventure': 'Movies - Action/Adventure',
 #'Movies_Anime_animation': 'Movies - Anime/Animation',
 #'Movies_Classics': 'Movies - Classics',
 #'Movies_Comedy': 'Movies - Comedy',
 #'Movies_Documentary': 'Movies - Documentary',
 #'Movies_Drama': 'Movies - Drama',
 #'Movies_Family': 'Movies - Family',
 #'Movies_Foreign': 'Movies - Foreign',
 #'Movies_Horror': 'Movies - Horror',
 #'Movies_Sci_fi_fantasy': 'Movies - Sci-Fi/Fantasy',
 #'Movies_Shorts': 'Movies - Shorts',
 #'Movies_Thriller': 'Movies - Thriller',
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

class Status(models.Model):
    """
    What Twitter made famous. Short messages, <160 characters, and
    meant to be sent out over such networks.
    """
    share_time = models.DateTimeField(default=datetime.datetime.now, help_text="Defaults to now.")
    text = models.CharField(max_length=160)
    is_published = models.BooleanField(editable=False, default=0)
    services = models.CharField(max_length=255, default="twitter,facebook", help_text="Comma seperated list of services to broadcast to.")

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['share_time']
        verbose_name_plural = "Statuses"

class Image(models.Model):
    """
    An image to post to a gallery somewhere.
    """
    share_time = models.DateTimeField(default=datetime.datetime.now, help_text="Defaults to now.")
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=UPLOAD_PATH % "images")
    description = models.TextField(help_text="The description of the photo.", blank=True)
    tags = models.CharField(max_length=255,help_text="Space-delimited list of tags. Tags that contain spaces need to be quoted. Ex. \"central station\" ", blank=True)
    is_public = models.BooleanField(default=1, help_text="True if photo is public, false if it is private. Default is public.")
    is_published = models.BooleanField(editable=False, default=0)
    services = models.CharField(max_length=255, default="flickr,twitter,facebook", help_text="Comma seperated list of services to broadcast to.")
    
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['share_time']

class Post(models.Model):
    """
    A block of text > 160 characters. Pushed out to blog posts,
    Facebook Notes, etc.
    """
    share_time = models.DateTimeField(default=datetime.datetime.now, help_text="Defaults to now.")
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_published = models.BooleanField(editable=False, default=0)
    services = models.CharField(max_length=255, default="twitter,facebook", help_text="Comma seperated list of services to broadcast to.")
    
    def __unicode__(self):
        return self.subject

    class Meta:
        ordering = ['share_time']

class Video(models.Model):
    """
    What it says on the tin.
    Push out to Flickr, YouTube, etc.
    """
    share_time = models.DateTimeField(default=datetime.datetime.now, help_text="Defaults to now.")
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=category_choices, help_text="Single cateogry this video belongs to.")
    description = models.TextField(blank=True, help_text="Short video description.")
    keywords = models.CharField(max_length=250, blank=True, help_text="Keywords seperated by comma.")
    video = models.FileField(upload_to = UPLOAD_PATH % "videos")
    is_published = models.BooleanField(editable=False, default=0)
    services = models.CharField(max_length=255, default="youtube,twitter,facebook", help_text="Comma seperated list of services to broadcast to.")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['share_time']

class Service(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="Service name. i.e youtube")
    is_authed = models.BooleanField(default=0)

    def __unicode__(self):
        return "Service: %s"  % ( self.name, )

    @models.permalink
    def get_authorize_url(self):
        return ("%s-authorize" % self.name.lower(),)

class Account(models.Model):
    user = models.CharField(max_length=255, blank=True)
    oauth_token = models.CharField(max_length=255, blank=True)
    oauth_secret = models.CharField(max_length=255, blank=True)
    authsub_token = models.CharField(max_length=255, blank=True)
    service_name = models.CharField(max_length=250, editable=False) 
    def __unicode__(self):
        return "Account: %s for %s"  % (self.user, self.service_name)


