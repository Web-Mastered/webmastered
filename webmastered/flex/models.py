from django.db import models
from django.http import HttpResponseRedirect

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel

from blocks.fields import FlexPageFields

class FlexPage(Page, FlexPageFields):
    """Flexibile page class."""

    template = "flex/flex_page.html"

    content_panels = Page.content_panels + FlexPageFields.content_panels

    class Meta:
        """ Meta FlexPage """
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"

class Anchor(Page):
    subpage_types = []
    parent_page_types = ['flex.FlexPage']
    
    page = models.ForeignKey('wagtailcore.Page', null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    anchor_id = models.CharField(max_length=255, default='', blank='False')

    content_panels = Page.content_panels + [
        PageChooserPanel('page'),
        FieldPanel('anchor_id')
    ]

    def get_sitemap_urls(self, request):
        return []

    def serve(self, request):
        if self.page is not None:
            path = str(self.page.get_url())
            if path.endswith('/'):
                path = path[:-1]
            anchor_path = path + "#" + self.anchor_id
            return HttpResponseRedirect(anchor_path)
        else:
            pass