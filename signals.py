"""post_save signal handlers for models."""

from sher.utils import get_auth_service
from django.db.models.signals import post_save
import sher.models

def status_handler(sender, instance, created, using, **kwargs):
    
    if instance.posted and created:

        #TODO: in the case of share time hoook django cron or some
        #task management system
        try:
        #twitter api
            api = get_auth_service(
                account_user="tsoporan",
                service="twitter",
            )
            api.PostUpdate(instance.text)

        except Exception, e:
            raise e

def post_handler(sender, instance, created, using, **kwargs):
    print "Post post_save called."

def image_handler(sender, instance, created, using, **kwargs):
    print "Image post_save called."

def video_handler(sender, instance, created, using, **kwargs):
    pass

post_save.connect(status_handler, sender=sher.models.Status)
post_save.connect(post_handler, sender="Post")
post_save.connect(image_handler, sender="Image")
post_save.connect(video_handler, sender="Video")

