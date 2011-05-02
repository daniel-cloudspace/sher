"""post_save signal handlers for models."""

from sher.utils import get_auth_service
from django.db.models.signals import post_save
import sher.models

#import logging

#TODO: in the case of share time hoook django cron or some
#task management system

def status_handler(sender, instance, created, using, **kwargs):
    
    if created:

        try:
            #twitter api
            #learn more: http://code.google.com/p/python-twitter/

            api = get_auth_service(
                account_user=instance.account.user,
                service = instance.account.service.name,
            )
            api.PostUpdate(instance.text)

        except Exception, e:
            #TODO: log instead, don't error on return
            raise e

def post_handler(sender, instance, created, using, **kwargs):

    if created:
        try:
            #facebook api
            #learn more: https://github.com/facebook/python-sdk
            api = get_auth_service(
                account_user = instance.account.user,
                service = instance.account.service.name,
            )

            api.put_object("me", "feed", message=instance.text)

        except Exception, e:
            raise e 
    
def image_handler(sender, instance, created, using, **kwargs):

    if created:
        #flickr api
        #learn more: http://flickrapi.sourceforge.net/
       
        try:
            api = get_auth_service(
                account_user = instance.account.user,
                service = instance.account.service.name,
            )
            api.upload(
                filename = str(instance.image.name),
                title = instance.title,
                description = instance.description,
                tags = instance.tags,
                is_public = 1 if instance.is_public else 0,
            )

        except Exception, e:
            raise e

def video_handler(sender, instance, created, using, **kwargs):
   
    import gdata.media
    import gdata.youtube

    if created:
    
        try:
            #gdata api
            #learn more: http://code.google.com/apis/youtube/1.0/developers_guide_python.html
            api =  get_auth_service(
                account_user = instance.account.user,
                service = instance.account.service.name,
            )
            categories = sher.models.categories #dict term:label mapping

            media_group = gdata.media.Group(
                title = gdata.media.Title(text=instance.title),
                description = gdata.media.Description(description_type="plain", text=instance.description),
                keywords = gdata.media.Keywords(text=instance.keywords),
                category = [
                    gdata.media.Category(
                        text=str(instance.category),
                        scheme="http://gdata.youtube.com/schemas/2007/categories.cat",
                        label=str(categories[instance.category]),
                    )
                ],
                player=None,
            )
            video_entry = gdata.youtube.YouTubeVideoEntry(media=media_group)
            video_file_path = instance.video.name
            
            entry = api.InsertVideoEntry(video_entry, video_file_path)
            
            upload_status = api.CheckUploadStatus(entry)
            if upload_status is not None:
                video_upload_state = upload_status[0]
                detailed_message = upload_status[1]
                print video_upload_state, detailed_message

        except Exception, e:
            raise e

post_save.connect(status_handler, sender=sher.models.Status)
post_save.connect(post_handler, sender=sher.models.Post)
post_save.connect(image_handler, sender=sher.models.Image)
post_save.connect(video_handler, sender=sher.models.Video)

