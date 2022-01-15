from django import template
from django.contrib import messages
from django.contrib.auth import get_user_model

from portal.models import Staff
from portal.forms import CustomStaffSettingsForm

register = template.Library()

@register.simple_tag
def get_staff():
    """returns the superuser models"""
    staff = Staff.objects.all()
    return staff


@register.simple_tag
def calculate_animation_delays(cardCount, cardWidth, delayInterval):
    """returns a list with animation delay values for AOS"""
    delay = 0
    delayList = []
    for card in range(cardCount):
        delayList.append(delay)
        delay = delay + delayInterval
        if (card + 1) == cardWidth:
            delay = 0
    return delayList


@register.filter
def index(indexable, i):
    return indexable[i]