from django.contrib import admin
from sher.models import Status, Post, Image, Video, Account, Service

class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'oauth_token']

admin.site.register(Status)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Video)
admin.site.register(Account)
admin.site.register(Service)
