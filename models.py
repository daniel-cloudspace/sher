from django.db import models


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


class Image(models.Model):
    """
    An image to post to a gallery somewhere.
    """
    share_time = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(blank=True, null=True)
    posted = models.BooleanField()
    title = models.CharField(max_length=100)
    image = models.ImageField()

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
    video = models.FileField()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['share_time']
