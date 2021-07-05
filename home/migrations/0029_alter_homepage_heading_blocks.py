# Generated by Django 3.2.4 on 2021-06-18 21:51

import blocks.fields
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_alter_homepage_heading_blocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='heading_blocks',
            field=wagtail.core.fields.StreamField([('heading_title', blocks.fields.HeadingTitleBlock()), ('heading_subtitle', blocks.fields.HeadingSubtitleBlock()), ('heading_featured_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Add a featured image.', required=True)), ('alt_text', wagtail.core.blocks.CharBlock(help_text='Displays this alternate text if the image cannot be displayed.', required=False)), ('caption', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'superscript', 'subscript', 'strikethrough'], help_text='Add an image caption.', required=False)), ('caption_align', wagtail.core.blocks.ChoiceBlock(choices=[('text-start', 'Left'), ('text-center', 'Centre'), ('text-end', 'Right')], label='Align the caption text.', required=False))]))], blank=True, help_text='Choose blocks to be shown at the top of the page.', null=True),
        ),
    ]
