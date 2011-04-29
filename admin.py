from django.contrib import admin
from sher.models import Status, Post, Image, Video, Account, Service

class StatusAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'account':
            kwargs['queryset'] = Account.objects.filter(service=Service.objects.get(name__iexact='twitter'))
        return super(StatusAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class PostAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'account':
            kwargs['queryset'] = Account.objects.filter(service=Service.objects.get(name__iexact='facebook'))
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class ImageAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'account':
            kwargs['queryset'] = Account.objects.filter(service=Service.objects.get(name__iexact='flickr'))
        return super(ImageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class VideoAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'account':
            kwargs['queryset'] = Account.objects.filter(service=Service.objects.get(name__iexact='youtube'))
        return super(VideoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'service', 'oauth_token']

admin.site.register(Status, StatusAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Service)
