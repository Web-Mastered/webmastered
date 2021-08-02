from django.db import models
from django import forms
from django.conf import settings

from wagtail.admin.edit_handlers import FieldPanel, HelpPanel, StreamFieldPanel, PageChooserPanel, MultiFieldPanel, InlinePanel
from wagtail.core.blocks.field_block import PageChooserBlock
from wagtail.core.fields import RichTextField, StreamField, StreamBlock
from wagtail.core.models import Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailstreamforms.blocks import WagtailFormBlock
from modelcluster.fields import ParentalManyToManyField, ParentalKey

from portal.models import PricingTable

class HeadingTitleBlock(blocks.RichTextBlock):
    """RichText heading block"""

    def __init__(self, required=True, help_text=None, editor="default", features=None, **kwargs):
        super().__init__(**kwargs)
        self.features = [
            "bold", 
            "italic", 
            "link",
            "superscript",
            "subscript",
            "strikethrough",
        ]

    class Meta:
        """ Meta HeadingTitleBlock """
        template = "streams/heading/heading_title_block.html"
        icon = "title"
        label = "Title"

class HeadingSubtitleBlock(blocks.RichTextBlock):
    """RichText heading block"""

    def __init__(self, required=True, help_text=None, editor="default", features=None, **kwargs):
        super().__init__(**kwargs)
        self.features = [
            "bold", 
            "italic", 
            "link",
            "superscript",
            "subscript",
            "strikethrough",
        ]

    class Meta:
        """ Meta HeadingSubtitleBlock """
        template = "streams/heading/heading_subtitle_block.html"
        icon = "title"
        label = "Subtitle"

class HeadingVariableBlock(blocks.RichTextBlock):
    """RichText heading block"""

    def __init__(self, required=True, help_text=None, editor="default", features=None, **kwargs):
        super().__init__(**kwargs)
        self.features = [
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "bold", 
            "italic", 
            "link",
            "superscript",
            "subscript",
            "strikethrough",
        ]

    class Meta:
        """ Meta HeadingVariableBlock """
        template = "streams/heading/heading_title_block.html"
        icon = "title"
        label = "Title"

class HeadingFeaturedImageBlock(blocks.StructBlock):
    """Images which take up the entire width of its parent"""

    align_options = (
        ("text-start", "Left"),
        ("text-center", "Centre"),
        ("text-end", "Right"),
    )

    image = ImageChooserBlock(required=True, help_text="Add a featured image.")
    alt_text = blocks.CharBlock(required=False,help_text="Displays this alternate text if the image cannot be displayed.")
    caption = blocks.RichTextBlock(features=['bold','italic','link','superscript','subscript','strikethrough'],required=False, help_text="Add an image caption.")
    caption_align = blocks.ChoiceBlock(label='Align the caption text.',required=False, choices=align_options)

    class Meta:
        """ Meta HeadingFeaturedImageBlock """
        template = "streams/heading/heading_featured_image_block.html"
        icon = "image"
        label = "Featured Image"

class HeadingCTAButtons(blocks.StructBlock):
    """Call-to-action (CTA) buttons for the heading hero"""

    class Button(blocks.StructBlock):

        button_style = (
            ("primary", "Primary"),
            ("secondary", "Secondary")
        )

        text = blocks.RichTextBlock(features=['bold','italic','link','superscript','subscript','strikethrough'],required=True, help_text="Add the text to be displayed in the button.")
        link = blocks.PageChooserBlock(required=False)
        style = blocks.ChoiceBlock(label='Choose a button style.',required=True, choices=button_style)

        class Meta:
            template = ""
            icon = "link"
            label = "Button"

    buttons = blocks.ListBlock(
        Button()
    )

    class Meta:
        template = "streams/heading/heading_cta_block.html"
        icon = "link"
        label = "Heading Buttons"

class BodyTitleBlock(blocks.RichTextBlock):
    """RichText title block"""

    def __init__(self, required=True, help_text=None, editor="default", features=None, **kwargs):
        super().__init__(**kwargs)
        self.features = [
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "bold", 
            "italic", 
            "link",
            "superscript",
            "subscript",
            "strikethrough",
        ]

    class Meta:
        """ Meta BodyTitleBlock """
        template = "streams/body/body_title_block.html"
        icon = "title"
        label = "Heading"

class BodyParagraphBlock(blocks.RichTextBlock):
    """RichText title block"""

    def __init__(self, **args):
        super().__init__(**args)
        self.features = [
            "bold", "italic", "lead",
            "ol", "ul", 
            "hr",
            "link", "document-link",
            "image", "embed",
            "code",
            "superscript", "subscript", "strikethrough",
            "blockquote"
        ]

    class Meta:
        """ Meta BodyParagraphBlock """
        template = "streams/body/body_paragraph_block.html"
        icon = "pilcrow"
        label = "Paragraph"

class BodyWideImageBlock(blocks.StructBlock):
    """Images which take up the entire width of its parent"""

    caption_align_options = (
        ("text-start", "Left"),
        ("text-center", "Centre"),
        ("text-end", "Right"),
    )

    image = ImageChooserBlock(required=True, help_text="Add an image.")
    alt_text = blocks.CharBlock(required=False,default="This is an image.",help_text="Displays this alternate text if the image cannot be displayed.")
    caption = blocks.RichTextBlock(features=['bold','italic','link','superscript','subscript','strikethrough'],required=False, help_text="Add an image caption.")
    caption_align = blocks.ChoiceBlock(label='Align the caption text.',required=False, choices=caption_align_options)

    class Meta:
        """ Meta BodyWideImageBlock """
        template = "streams/body/body_wide_image_block.html"
        icon = "image"
        label = "Wide Image"

class BodyImageAndTextBlock(blocks.StructBlock):
    """Images which take up the entire width of its parent"""

    align_options = (
        ("image-left", "Image - Text"),
        ("image-right", "Text - Image"),
    )

    image = ImageChooserBlock(required=True, help_text="Add an image.")
    alt_text = blocks.CharBlock(required=False,default="This is an image.",help_text="Displays this alternate text if the image cannot be displayed.")
    caption = blocks.RichTextBlock(features=['bold','italic','link','superscript','subscript','strikethrough'],required=False, help_text="Add an image caption.")
    text = BodyParagraphBlock(required=True,help_text="Add some text to display beside the image.")
    alignment = blocks.ChoiceBlock(label='Align the image and text.',required=False, choices=align_options)

    class Meta:
        """ Meta BodyImageAndTextBlock """
        template = "streams/body/body_image_text_block.html"
        icon = "image"
        label = "Image & Text"


class BodyFullWidthCardGrid(blocks.StructBlock):
    """A full width block displaying a card grid"""

    class Card(blocks.StructBlock):

        image = ImageChooserBlock(required=False, help_text="Add an image.")
        title = BodyParagraphBlock(required=False,help_text="Add some text for the card's title.",label="Card title")
        text = BodyParagraphBlock(required=False,help_text="Add some text for the card's body.",label="Card body")
        animated = blocks.BooleanBlock(required=False,default=True,blank=True,null=True,help_text="Select to animate on scroll.")

        class Meta:
            template = ""
            icon = "placeholder"
            label = "Card"

    secondary_background_theme = blocks.BooleanBlock(default=True,blank=False,null=False)
    cards = blocks.ListBlock(
        Card()
    )
    
    class Meta:
        template = "streams/body/body_fw_card_grid_block.html"
        icon = "table"
        label = "Full Width Card Grid"


class BodyTextAndFormBlock(blocks.StructBlock):
    """Form and text block"""

    align_options = (
        ("form-left", "Form - Text"),
        ("form-right", "Text - Form"),
    )

    form = WagtailFormBlock()
    title = BodyTitleBlock(required=True,help_text="Add a title to display above the form.",label="Form Widget Title")
    text = BodyParagraphBlock(required=True,help_text="Add some text to display beside the form, under the title.",label="Form Widget Body Text")
    alignment = blocks.ChoiceBlock(label='Align the image and text.',required=False, choices=align_options)

    class Meta:
        """ Meta BodyTextAndFormBlock """
        template = "streams/body/body_form_text_block.html"
        icon = "image"
        label = "Form & Text"



class BodyFullWidthStaffCardBlock(blocks.StructBlock):
    """Staff list card grid"""

    title = BodyTitleBlock(required=True,help_text="Add a title to display above the staff card grid.",label="Title")
    animated = blocks.BooleanBlock(required=False,default=True,blank=True,null=True,help_text="Select to animate on scroll.")

    class Meta:
        """ Meta BodyFullWidthSuperuserCardBlock """
        template = "streams/body/body_fw_staff_card_block.html"
        icon = "user"
        label = "Full Width Staff Card Grid"


class BodyHTMLBlock(blocks.RawHTMLBlock):
    def __init__(self, required=True, help_text=None, editor="default", features=None, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        template = "streams/body/body_html_block.html"
        icon = "code"
        label = "Raw HTML"


class BodyPricingBlock(blocks.StructBlock):
    pricing_tables = []
    try:
        if PricingTable.objects.filter().exists():
            for table in PricingTable.objects.all():
                this_tuple = tuple((table.html_table, table.name))
                pricing_tables.append(this_tuple)
    except:
        pass

    tuple(pricing_tables)

    table = blocks.ChoiceBlock(label='Choose from the list of available pricing tables.',required=False, choices=pricing_tables)

    class Meta:
        template = "streams/body/body_pricing_block.html"
        icon = "table"
        label = "Pricing Table"


class BodyTimelineCardBlock(blocks.StructBlock):
    """A block displaying a card grid for timeline"""

    class Event(blocks.StructBlock):

        image = ImageChooserBlock(required=False, help_text="Add an image.")
        title = HeadingVariableBlock(required=False,help_text="Add some text for the event card's title.",label="Card title")
        text = BodyParagraphBlock(required=False,help_text="Add some text for the event card's body.",label="Card body")
        animated = blocks.BooleanBlock(required=False,default=True,blank=True,null=True,help_text="Select to animate on scroll.")

        class Meta:
            template = ""
            icon = "time"
            label = "Event"

    events = blocks.ListBlock(
        Event()
    )
    
    class Meta:
        template = "streams/body/body_timeline_card_block.html"
        icon = "date"
        label = "Timeline Cards"



page_heading_blocks = StreamField(
    [
        ("heading_title", HeadingTitleBlock()),
        ("heading_subtitle", HeadingSubtitleBlock()),
        ("heading_featured_image", HeadingFeaturedImageBlock()),
        ("heading_cta_buttons", HeadingCTAButtons()),
    ], block_counts = {
        'heading_title' : {'min_num': 1, 'max_num': 1},
        'heading_subtitle' : {'min_num': 0, 'max_num': 1},
        'heading_featured_image' : {'min_num': 0, 'max_num': 1},
    },
    null = True,
    blank = True,
    help_text = "Choose blocks to be shown at the top of the page."
)

page_body_blocks = StreamField(
    [
        ("body_title", BodyTitleBlock()),
        ("body_paragraph", BodyParagraphBlock()),
        ("body_wide_image", BodyWideImageBlock()),
        ("body_image_text", BodyImageAndTextBlock()),
        ("fw_card_grid", BodyFullWidthCardGrid()),
        ('form_text', BodyTextAndFormBlock()),
        ('fw_staff_card_grid', BodyFullWidthStaffCardBlock()),
        ('raw_html', BodyHTMLBlock()),
        ('pricing_table_html', BodyPricingBlock()),
        ('body_timeline_card', BodyTimelineCardBlock()),
    ],
    null = True,
    blank = True,
    help_text = "Choose blocks to be shown in the body."
)

class HomePageFields(models.Model):
    """HomePage field definitions"""

    heading_blocks = page_heading_blocks
    body_blocks = page_body_blocks

    content_panels = [
        MultiFieldPanel(
            [
                StreamFieldPanel("heading_blocks", classname=""),
            ],
            heading="Page Heading",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                StreamFieldPanel("body_blocks", classname=""),
            ],
            heading="Page Body",
            classname="collapsible",
        ),
    ]

    class Meta:
        """ Meta HomePageFields """
        abstract = True


class FlexPageFields(models.Model):
    """FlexPage field definitions"""

    heading_blocks = page_heading_blocks
    body_blocks = page_body_blocks

    content_panels = [
        MultiFieldPanel(
            [
                StreamFieldPanel("heading_blocks", classname=""),
            ],
            heading="Page Heading",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                StreamFieldPanel("body_blocks", classname=""),
            ],
            heading="Page Body",
            classname="collapsible",
        ),
    ]

    class Meta:
        """ Meta FlexPageFields """
        abstract = True


class BlogListingPageFields(models.Model):
    """Blog Listing Page field definitions"""

    heading_blocks = page_heading_blocks

    content_panels = [
        MultiFieldPanel(
            [
                StreamFieldPanel("heading_blocks", classname=""),
            ],
            heading="Page Heading",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                HelpPanel(content="<h2>The page body consists of a list blog posts in date order, newest at the top.</h2>"),
            ],
            heading="Page Body",
            classname="collapsible",
        ),
    ]

    class Meta:
        """ Meta BlogListingPageFields """
        abstract = True

class BlogPostPageFields(models.Model):
    """Blog Post Page field definitions"""

    heading_blocks = page_heading_blocks
    body_blocks = page_body_blocks

    enable_comments = models.BooleanField(default=True,blank=False,null=False)

    categories = ParentalManyToManyField("blog.BlogPostCategory", blank=True)

    content_panels = [
        MultiFieldPanel(
            [
                StreamFieldPanel("heading_blocks", classname=""),
            ],
            heading="Page Heading",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                StreamFieldPanel("body_blocks", classname=""),
            ],
            heading="Page Body",
            classname="collapsible",
        ),
    ]

    if settings.ENABLE_EXPERIMENTAL_BLOG_COMMENTING:
        settings_panels = [
            FieldPanel("enable_comments"),
        ]
    else:        
        settings_panels = []


    promote_panels = [
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],heading="Assign Categories"
        )
    ]

    class Meta:
        """ Meta BlogPostPageFields """
        abstract = True



