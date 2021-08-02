# Generated by Django 3.2.4 on 2021-07-29 12:30

import blocks.fields
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtailstreamforms.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0003_alter_flexpage_body_blocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flexpage',
            name='body_blocks',
            field=wagtail.core.fields.StreamField([('body_title', blocks.fields.BodyTitleBlock()), ('body_paragraph', blocks.fields.BodyParagraphBlock()), ('body_wide_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Add an image.', required=True)), ('alt_text', wagtail.core.blocks.CharBlock(default='This is an image.', help_text='Displays this alternate text if the image cannot be displayed.', required=False)), ('caption', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'superscript', 'subscript', 'strikethrough'], help_text='Add an image caption.', required=False)), ('caption_align', wagtail.core.blocks.ChoiceBlock(choices=[('text-start', 'Left'), ('text-center', 'Centre'), ('text-end', 'Right')], label='Align the caption text.', required=False))])), ('body_image_text', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Add an image.', required=True)), ('alt_text', wagtail.core.blocks.CharBlock(default='This is an image.', help_text='Displays this alternate text if the image cannot be displayed.', required=False)), ('caption', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'superscript', 'subscript', 'strikethrough'], help_text='Add an image caption.', required=False)), ('text', blocks.fields.BodyParagraphBlock(help_text='Add some text to display beside the image.', required=True)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('image-left', 'Image - Text'), ('image-right', 'Text - Image')], label='Align the image and text.', required=False))])), ('fw_card_grid', wagtail.core.blocks.StructBlock([('secondary_background_theme', wagtail.core.blocks.BooleanBlock(blank=False, default=True, null=False)), ('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Add an image.', required=False)), ('title', blocks.fields.BodyParagraphBlock(help_text="Add some text for the card's title.", label='Card title', required=False)), ('text', blocks.fields.BodyParagraphBlock(help_text="Add some text for the card's body.", label='Card body', required=False)), ('animated', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Select to animate on scroll.', null=True, required=False))])))])), ('form_text', wagtail.core.blocks.StructBlock([('form', wagtail.core.blocks.StructBlock([('form', wagtailstreamforms.blocks.FormChooserBlock()), ('form_action', wagtail.core.blocks.CharBlock(help_text='The form post action. "" or "." for the current page or a url', required=False)), ('form_reference', wagtailstreamforms.blocks.InfoBlock(help_text='This form will be given a unique reference once saved', required=False))])), ('title', blocks.fields.BodyTitleBlock(help_text='Add a title to display above the form.', label='Form Widget Title', required=True)), ('text', blocks.fields.BodyParagraphBlock(help_text='Add some text to display beside the form, under the title.', label='Form Widget Body Text', required=True)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('form-left', 'Form - Text'), ('form-right', 'Text - Form')], label='Align the image and text.', required=False))])), ('fw_staff_card_grid', wagtail.core.blocks.StructBlock([('title', blocks.fields.BodyTitleBlock(help_text='Add a title to display above the staff card grid.', label='Title', required=True)), ('animated', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Select to animate on scroll.', null=True, required=False))])), ('raw_html', blocks.fields.BodyHTMLBlock()), ('pricing_table_html', blocks.fields.BodyPricingBlock())], blank=True, help_text='Choose blocks to be shown in the body.', null=True),
        ),
    ]
