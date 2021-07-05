from django.db import models
from django import forms
from django.conf import settings

from wagtail.admin.edit_handlers import FieldPanel, HelpPanel, StreamFieldPanel, PageChooserPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField, StreamField, StreamBlock
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

from modelcluster.fields import ParentalManyToManyField

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
            "bold", "italic",
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

page_heading_blocks = StreamField(
    [
        ("heading_title", HeadingTitleBlock()),
        ("heading_subtitle", HeadingSubtitleBlock()),
        ("heading_featured_image", HeadingFeaturedImageBlock())
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

