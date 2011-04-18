from django.db import models
from django.conf import settings
from os.path import join

UPLOAD_PATH = join(settings.MEDIA_ROOT, "%s")

class Status(models.Model):
    """
    What Twitter made famous. Short messages, <160 characters, and
    meant to be sent out over such networks.
    """
    share_time = models.DateTimeField(auto_now_add=True)
    posted = models.BooleanField()
    text = models.CharField(max_length=160)

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
    posted = models.BooleanField()
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=UPLOAD_PATH % "images")

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
    posted = models.BooleanField()
    subject = models.CharField(max_length=160)
    body = models.TextField()

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
    posted = models.BooleanField()
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, help_text="Single cateogry this video belongs to.")
    description = models.TextField(blank=True, help_text="Short video description.")
    keywords = models.CharField(max_length=250, blank=True, help_text="Keywords seperated by comma.")
    video = models.FileField(upload_to = UPLOAD_PATH % "videos")

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['share_time']

    #If posted, connect to signal.

class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_authorize_url(self):
        return ("%s-authorize" % self.name.lower(),)

class Account(models.Model):
    user = models.CharField(max_length=255, blank=True)
    oauth_token = models.CharField(max_length=255, blank=True)
    oauth_secret = models.CharField(max_length=255, blank=True)
    authsub_token = models.CharField(max_length=255, blank=True)
    service = models.ForeignKey(Service)   
 
    def __unicode__(self):
        return "%s - %s " % (self.user, self.service)
    


