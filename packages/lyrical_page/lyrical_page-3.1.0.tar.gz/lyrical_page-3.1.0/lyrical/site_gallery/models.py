from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import SingleRelatedObjectDescriptor
from django.db.models.query import QuerySet
from filebrowser.fields import FileBrowseField
from lyrical.site_content.models import InheritanceQuerySet

from lyrical.site_content import register_template_tag_library

class SiteGallery(models.Model):
    code = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    custom_template = models.CharField(max_length=255, blank=True, null=True)
    css_class = models.CharField(max_length=255, blank=True, null=True)

    @property
    def items(self):
        return InheritanceQuerySet(SiteGalleryItem).filter(gallery=self).select_subclasses()

    @property
    def embed_code(self):
        if not self.code:
            return ''
        return "{{% site_gallery '{0}' %}}".format(self.code)

    def __unicode__(self):
        return u'%s' % (self.title)

    class Meta:
        verbose_name_plural = 'Site Galleries'

class SiteGalleryItem(models.Model):
    gallery = models.ForeignKey(SiteGallery)
    title = models.CharField(max_length=255, blank=True)
    caption = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)

    def html_tag(self):
        return ''

    def item_type(self):
        return self.__class__.__name__

    def __unicode__(self):
        return u'%s' % (self.caption)

class SiteGalleryImageItem(SiteGalleryItem):
    image = FileBrowseField(format='image', max_length=255)
    thumbnail = FileBrowseField(format='image', max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.thumbnail:
            self.thumbnail = self.image
        return super(SiteGalleryImageItem, self).save(*args, **kwargs)

    @property
    def img_src(self):
        return self.image.url

    @property
    def html_tag(self):
        return '<img src="{0}">'.format(self.image.url)

    def __unicode__(self):
        return u'%s' % (self.image)

class SiteGalleryYoutubeItem(SiteGalleryItem):
    video_id = models.CharField(max_length=200, blank=False)
    thumbnail = FileBrowseField(format='image', max_length=255, blank=True)

    def html_tag(self):
        return self.video_id

    def __unicode__(self):
        return u'%s' % (self.video_id)

class SiteGalleryVideoItem(SiteGalleryItem):
    video = models.TextField(blank=True)
    thumbnail = FileBrowseField(format='image', max_length=255, blank=True)

    def html_tag(self):
        return self.video

    def __unicode__(self):
        return u'%s' % (self.video)

register_template_tag_library('site_gallery')
