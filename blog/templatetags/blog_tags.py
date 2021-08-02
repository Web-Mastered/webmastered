from django import template
from django.conf import settings

register = template.Library()

title = ""
featured_img_url = ""
subtitle = ""

@register.simple_tag
def set_featured_img_url(val=None):
    """Allows featured image URL to be stored"""
    global featured_img_url
    featured_img_url = val
    return True

@register.simple_tag
def get_featured_img_url():
    """Allows featured image URL to be retrieved"""
    global featured_img_url
    this_featured_img_url = featured_img_url
    featured_img_url = None
    return this_featured_img_url

@register.simple_tag
def set_title(val=None):
    """Allows title text to be stored"""
    global title
    title = val
    return True

@register.simple_tag
def get_title():
    """Allows title text to be retrieved"""
    global title
    this_title = title
    title = None
    return this_title

@register.simple_tag
def set_subtitle(val=None):
    """Allows subtitle text to be stored"""
    global subtitle
    subtitle = val
    return True

@register.simple_tag
def get_subtitle():
    """Allows subtitle text to be retrieved"""
    global subtitle
    this_subtitle = subtitle
    subtitle = None
    return this_subtitle

@register.simple_tag
def experimental_comments_status():
    """Returns the global enable/disable status of the comments system"""
    commenting_status = settings.ENABLE_EXPERIMENTAL_BLOG_COMMENTING
    return commenting_status

