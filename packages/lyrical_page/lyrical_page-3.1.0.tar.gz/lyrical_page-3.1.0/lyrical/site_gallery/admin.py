from django.contrib import admin
from django.conf import settings
from django import forms
from django.db import models as django_models
import models
from lyrical.site_content.settings import ENABLE_BUILTIN_MEDIA, RTE_CONFIG_URI

class SiteGalleryImageInline(admin.TabularInline):
    model = models.SiteGalleryImageItem
    formfield_overrides = {
            django_models.TextField: {'widget': forms.TextInput},
        }

class SiteGalleryVideoInline(admin.TabularInline):
    model = models.SiteGalleryVideoItem
    formfield_overrides = {
            django_models.TextField: {'widget': forms.TextInput},
        }

class SiteGalleryYoutubeVideoInline(admin.TabularInline):
    model = models.SiteGalleryYoutubeItem
    formfield_overrides = {
            django_models.TextField: {'widget': forms.TextInput},
        }

class SiteGalleryAdmin(admin.ModelAdmin):
    inlines = [SiteGalleryImageInline, SiteGalleryVideoInline,
            SiteGalleryYoutubeVideoInline]
    readonly_fields = ['embed_code']
    list_display = ('__str__', 'embed_code')

    if ENABLE_BUILTIN_MEDIA:
        class Media:
            css = {'all': ('site_content/css/grappelli-tinymce.css',)}
            js = (getattr(settings, 'STATIC_URL', '') + 'grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', RTE_CONFIG_URI)

admin.site.register(models.SiteGallery, SiteGalleryAdmin)
