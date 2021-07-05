from django.db import models
from wagtail.core.models import Page
from blocks.fields import FlexPageFields

class FlexPage(Page, FlexPageFields):
    """Flexibile page class."""

    template = "flex/flex_page.html"

    content_panels = Page.content_panels + FlexPageFields.content_panels

    class Meta:
        """ Meta FlexPage """
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"