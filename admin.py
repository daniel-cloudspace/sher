from django.contrib import admin
from sher.models import Status, Post, Image, Video, Account, Service

class StatusAdmin(admin.ModelAdmin):
    list_display = ['text', 'share_time', 'is_published']

class PostAdmin(admin.ModelAdmin):
    list_display = []

class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'share_time', 'image', 'is_public', 'is_published']

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'share_time', 'category', 'video', 'is_published']

class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'oauth_token', 'oauth_secret', 'authsub_token', 'service_name']

admin.site.register(Status, StatusAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Account, AccountAdmin)
