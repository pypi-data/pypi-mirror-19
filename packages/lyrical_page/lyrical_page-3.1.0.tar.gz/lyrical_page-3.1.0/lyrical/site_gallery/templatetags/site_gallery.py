from django import template
from django.template import loader
from django.conf import settings

from lyrical.site_gallery.models import SiteGallery

register = template.Library()

@register.simple_tag(takes_context=True)
def site_gallery(context, code):
    template_name = 'site_gallery/tag_site_gallery.html'
    try:
        gallery = SiteGallery.objects.get(code=code)
        if gallery.custom_template:
            template_name = gallery.custom_template
    except SiteGallery.DoesNotExist:
        gallery = None

    return loader.render_to_string(template_name, { 'gallery': gallery})


