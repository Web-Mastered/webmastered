from django.db import models
from django.db.models.fields import CharField, EmailField, URLField

from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import EditHandler, FieldPanel, FieldRowPanel, HelpPanel, TabbedInterface, ObjectList, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail.core.models import Orderable
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from dashboard.metrics import get_cpu, get_ram

class SocialMediaAccount(Orderable):
    schema_settings = ParentalKey("WebsiteSettings", related_name="social_accounts")
    account_provider = CharField(
        help_text="Provider of the account, e.g. Facebook, Instagram, LinkedIn, etc.",
        max_length=100,
        blank=False,
        null=False,
    )
    account_username = CharField(
        help_text="Username or handle of the account.",
        max_length=100,
        blank=False,
        null=False,
    )
    account_url = URLField(
        help_text="URL link to the account profile.",
        max_length=200,
        blank=False,
        null=False,
        verbose_name="Account URL"
    )

class LinkedURL(Orderable):
    schema_settings = ParentalKey("WebsiteSettings", related_name="linked_url")
    link = URLField(help_text="URL of a reference Web page that unambiguously indicates the item's identity.", verbose_name="Linked URL", max_length=100, null=True, blank=True)

class Contact(Orderable):
    schema_settings = ParentalKey("WebsiteSettings", related_name="contact_point")
    contact_type = CharField(help_text="Specify the type, e.g. technical support, billing support, sales, etc.", max_length=100, null=False, blank=False)
    email = EmailField(max_length=254, help_text="Email address for this contact point.", null=False, blank=False)
    telephone = CharField(help_text="Telephone number for this contact point.", max_length=100, null=True, blank=True)

@register_setting
class WebsiteSettings(BaseSetting, ClusterableModel):
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

    organisation_legal_name = CharField(verbose_name="Organisation Legal name", help_text="The official name of the organization, e.g. the registered company name.", max_length=100, null=True, blank=True)
    organisation_alternate_name = CharField(verbose_name="Alternative organisation name", help_text="Another name the organisation goes by.", max_length=100, null=True, blank=True)

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

    analytics_panels = [
        FieldRowPanel([
            FieldPanel("tracking_id"),
        ], heading="Google Analytics"),
    ]

    socials_panels = [
        FieldRowPanel([
            InlinePanel("social_accounts", label="Social Media Accounts"),
        ], heading="Social Media Accounts")
    ]

    schema_panels = [
        FieldRowPanel([
            FieldPanel("organisation_legal_name", classname="col6"),
            FieldPanel("organisation_alternate_name", classname="col6"),
            InlinePanel("linked_url", label="Linked URLs", classname="col8"),
            HelpPanel(heading="Note", content='<p>Social media account links will also be automatically appended to the list of linked URLs.</p>', classname="col4"),
            InlinePanel("contact_point", label="Contact Points", classname="col12"),
        ], heading="Organisation")
    ]

    edit_handler = TabbedInterface([
        ObjectList(look_and_feel_panels, heading="Look & Feel"),
        ObjectList(analytics_panels, heading="Analytics"),
        ObjectList(socials_panels, heading="Social Media"),
        ObjectList(schema_panels, heading="Schema"),
    ])

    class Meta:
        """ Meta WebsiteSettings """
        verbose_name = 'Website Settings'

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
