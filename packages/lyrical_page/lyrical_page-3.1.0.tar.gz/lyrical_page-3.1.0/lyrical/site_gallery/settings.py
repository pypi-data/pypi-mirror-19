from django.conf import settings

THUMBNAIL_SIZE = getattr(settings, 'SITE_GALLERY_THUMBNAIL_SIZE', None)
