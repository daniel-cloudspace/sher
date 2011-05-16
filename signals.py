"""post_save signal handlers for models."""

from django.db.models.signals import post_save, m2m_changed
import sher.models
import sher.utils

from sher.tasks import status_task, image_task, video_task

import logging

def status_handler(sender, instance, created, using, **kwargs):

    services = sher.utils.get_services_list(instance.services)

    if created:
        status_task.apply_async(args=[instance, services], eta=instance.share_time)

def image_handler(sender, instance, created, using, **kwargs):
    
    services = sher.utils.get_services_list(instance.services)

    if created:
        image_task.apply_async(args=[instance, services], eta=instance.share_time)

def video_handler(sender, instance, created, using, **kwargs):
    
    services = sher.utils.get_services_list(instance.services)
   
    if created:
        video_task.apply_async(args=[instance, services], eta=instance.share_time)

def post_handler(sender, instance, created, **kwargs):  
    #not impemented yet
    pass


post_save.connect(receiver=status_handler, sender=sher.models.Status)
post_save.connect(receiver=post_handler, sender=sher.models.Post)
post_save.connect(receiver=image_handler, sender=sher.models.Image)
post_save.connect(receiver=video_handler, sender=sher.models.Video)

