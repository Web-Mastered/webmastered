from django.db import models
from wagtail.core.models import Page
from blocks.fields import HomePageFields

class HomePage(Page, HomePageFields):
    """HomePage class"""

    template = "home/home_page.html"
    max_count = 1

    subpage_types = [
        'flex.FlexPage',
        'blog.BlogListingPage',
    ]
    parent_page_type = [
        'wagtailcore.Page',
    ]

    content_panels = Page.content_panels + HomePageFields.content_panels

    class Meta:
        """ Meta HomePage """
        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"