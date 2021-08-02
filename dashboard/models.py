from django.db import models

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import EditHandler, FieldPanel, FieldRowPanel, HelpPanel, TabbedInterface, ObjectList
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel

from dashboard.metrics import get_cpu, get_ram

@register_setting
class WebsiteSettings(BaseSetting):
    logo = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="Choose an image for the site logo. This logo will be displayed at various places around the website."
    )

    site_icon = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="Site icons are what you see in browser tabs and bookmark bars, please upload a square image."
    )

    primary = ColorField(default="#0d6efd", help_text="default is #0d6efd")
    secondary = ColorField(default="#6c757d", help_text="default is #6c757d")
    success = ColorField(default="#198754", help_text="default is #198754")
    info = ColorField(default="#0dcaf0", help_text="default is #0dcaf0")
    warning = ColorField(default="#ffc107", help_text="default is #ffc107")
    danger = ColorField(default="#dc3545", help_text="default is #dc3545")
    light = ColorField(default="#f8f9fa", help_text="default is #f8f9fa")
    dark = ColorField(default="#212529", help_text="default is #212529")

    tracking_id = models.CharField(
        max_length=24,
        help_text="Enter your Google Analytics Tracking ID here, it should look something like this: UA-000000-2",
        null=True,
        blank=True,
        verbose_name="Tracking ID"
    )

    look_and_feel_panels = [
        FieldRowPanel([
            ImageChooserPanel("logo"),
            ImageChooserPanel("site_icon")
        ], heading="Branding"),
        FieldRowPanel([
            NativeColorPanel('primary', classname="col6"),
            NativeColorPanel('secondary', classname="col6"),
            NativeColorPanel('success', classname="col6"),
            NativeColorPanel('info', classname="col6"),
            NativeColorPanel('warning', classname="col6"),
            NativeColorPanel('danger', classname="col6"),
            NativeColorPanel('light', classname="col6"),
            NativeColorPanel('dark', classname="col6"),
        ], heading="Colours"),
    ]

    class Meta:
        """ Meta WebsiteSettings """
        verbose_name = 'Website Settings'



    analytics_panels = [
        FieldRowPanel([
            FieldPanel("tracking_id"),
        ], heading="Google Analytics"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(look_and_feel_panels, heading="Look & Feel"),
        ObjectList(analytics_panels, heading="Analytics"),
    ])


@register_setting(icon='site')
class Metrics(BaseSetting):
    """Displays system metrics such as CPU, RAM and disk utilisation"""
    panels = [
        HelpPanel(
            template='engine/metrics.html',
        )
    ]

    class Meta:
        """ Meta Metrics """
        verbose_name = 'Engine Metrics'



@register_setting(icon='help')
class AboutEngine(BaseSetting):
    """
    This class displays a HelpPanel in a newly created settings tab "About Engine"
    the HelpPanel displays various information regarding Engine.
    """
    panels = [
        HelpPanel(
            template='engine/about.html',
        )
    ]

    class Meta:
        """ Meta AboutEngine """
        verbose_name = 'About Engine'
