from celery.decorators import task

import logging

from sher.utils import get_services, get_account, get_services_list
from sher.utils import shorten_url as _s
import sher.models

#TODO: - logging

@task
def status_task(instance):

    services = get_services_list(instance.services)
    sdict = get_services(services)
    
    post_msg = instance.text

    tw_api = sdict.get('twitter', None)
    fb_api = sdict.get('facebook', None)

    try:
        if tw_api:
            tw_api.PostUpdate(post_msg)

        if fb_api:
            fb_api.put_object("me", "feed", message=post_msg)

        instance.is_published = True
        instance.save()

    except Exception, e:
        raise e

@task
def image_task(instance):
   
    services = get_services_list(instance.services)
    sdict = get_services(services)
    
    fl_api = sdict.get('flickr', None)
    tw_api = sdict.get('twitter', None)
    fb_api = sdict.get('facebook', None)
   
    post_msg = "New image posted check it out: %s"


    if fl_api:
        try:
            
            fl_api.upload(
                filename = str(instance.image.name),
                title = instance.title,
                description = instance.description,
                tags = instance.tags,
                is_public = 1 if instance.is_public else 0,
            )

            flickr_photo_url = "http://www.flickr.com/photos/%s/%s/"

            user = fl_api.photos_search(user_id="me") #get photos of authed user
            photos = user.find('photos')
            
            last_photo = photos.getchildren()[0] 
            owner_id = last_photo.attrib['owner']
            photo_id = last_photo.attrib['id']

            #post twitter and facebook image url
            post_msg = post_msg % _s(flickr_photo_url % (owner_id, photo_id))

            if tw_api:
                tw_api.PostUpdate(post_msg)
            
            if fb_api:
                fb_api.put_object("me", "feed", message=post_msg)
            
            instance.is_published = True #update instance
            instance.save()

        except Exception, e:
            raise e


@task
def post_task():
    pass #not implemented yet

@task
def video_task(instance):
    
    services = get_services_list(instance.services)
    sdict = get_services(services)
    
    yt_api = sdict.get('youtube', None)
    tw_api = sdict.get('twitter', None)
    fb_api = sdict.get('facebook', None)

    import gdata.media
    import gdata.youtube

    post_msg = "New video check it out: %s"

    if yt_api:

        try:
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
            
            entry = yt_api.InsertVideoEntry(video_entry, video_file_path)
            
            account = get_account("youtube")
            videos = yt_api.GetYouTubeUserFeed(username=account.user)
            entry = videos.entry[0]
            link = entry.GetHtmlLink().href

            #post twitter/facebook youtube link
            post_msg = post_msg % _s(link)
            
            if tw_api:
                tw_api.PostUpdate(post_msg)
            
            if fb_api:
                fb_api.put_object("me", "feed", message=post_msg)
            
            instance.is_published = True #update instance obj
            instance.save()
        except Exception, e:
            raise e


