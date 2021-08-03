# Generated by Django 3.2.4 on 2021-08-03 10:49

import blocks.fields
from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtailstreamforms.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blogpostpage_body_blocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpostpage',
            name='body_blocks',
            field=wagtail.core.fields.StreamField([('body_title', blocks.fields.BodyTitleBlock()), ('body_paragraph', blocks.fields.BodyParagraphBlock()), ('body_wide_image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Add an image.', required=True)), ('alt_text', wagtail.core.blocks.CharBlock(default='This is an image.', help_text='Displays this alternate text if the image cannot be displayed.', required=False)), ('caption', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'superscript', 'subscript', 'strikethrough'], help_text='Add an image caption.', required=False)), ('caption_align', wagtail.core.blocks.ChoiceBlock(choices=[('text-start', 'Left'), ('text-center', 'Centre'), ('text-end', 'Right')], label='Align the caption text.', required=False))])), ('body_image_text', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Add an image.', required=True)), ('alt_text', wagtail.core.blocks.CharBlock(default='This is an image.', help_text='Displays this alternate text if the image cannot be displayed.', required=False)), ('caption', wagtail.core.blocks.RichTextBlock(features=['bold', 'italic', 'link', 'superscript', 'subscript', 'strikethrough'], help_text='Add an image caption.', required=False)), ('text', blocks.fields.BodyParagraphBlock(help_text='Add some text to display beside the image.', required=True)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('image-left', 'Image - Text'), ('image-right', 'Text - Image')], label='Align the image and text.', required=False))])), ('fw_card_grid', wagtail.core.blocks.StructBlock([('secondary_background_theme', wagtail.core.blocks.BooleanBlock(blank=False, default=True, null=False)), ('cards', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Add an image.', required=False)), ('title', blocks.fields.BodyParagraphBlock(help_text="Add some text for the card's title.", label='Card title', required=False)), ('text', blocks.fields.BodyParagraphBlock(help_text="Add some text for the card's body.", label='Card body', required=False)), ('animated', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Select to animate on scroll.', null=True, required=False))])))])), ('form_text', wagtail.core.blocks.StructBlock([('form', wagtail.core.blocks.StructBlock([('form', wagtailstreamforms.blocks.FormChooserBlock()), ('form_action', wagtail.core.blocks.CharBlock(help_text='The form post action. "" or "." for the current page or a url', required=False)), ('form_reference', wagtailstreamforms.blocks.InfoBlock(help_text='This form will be given a unique reference once saved', required=False))])), ('title', blocks.fields.BodyTitleBlock(help_text='Add a title to display above the form.', label='Form Widget Title', required=True)), ('text', blocks.fields.BodyParagraphBlock(help_text='Add some text to display beside the form, under the title.', label='Form Widget Body Text', required=True)), ('alignment', wagtail.core.blocks.ChoiceBlock(choices=[('form-left', 'Form - Text'), ('form-right', 'Text - Form')], label='Align the image and text.', required=False))])), ('fw_staff_card_grid', wagtail.core.blocks.StructBlock([('title', blocks.fields.BodyTitleBlock(help_text='Add a title to display above the staff card grid.', label='Title', required=True)), ('animated', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Select to animate on scroll.', null=True, required=False))])), ('raw_html', blocks.fields.BodyHTMLBlock()), ('pricing_table_html', wagtail.core.blocks.StructBlock([('table', wagtail.core.blocks.ChoiceBlock(choices=[('<table class="table">\r\n                                <thead>\r\n                                    <tr>\r\n                                        <th scope="col" style="width: 25%"></th>\r\n                                        <th scope="col" class="text-center" style="width: 25%">Basic</th>\r\n                                        <th scope="col" class="text-center" style="width: 25%">Standard</th>\r\n                                        <th scope="col" class="text-center" style="width: 25%">Professional</th>\r\n                                    </tr>\r\n                                </thead>\r\n                                <tbody>\r\n                                    <tr>\r\n                                        <th scope="row"></th>\r\n                                        <td class="text-center text-wrap">\r\n                                            Great for small and light websites with very little visitors, allowing for a simple and affordable\r\n                                            way to establish a digital presence.\r\n                                        </td>\r\n                                        <td class="text-center text-wrap">\r\n                                            Great for slighly larger websites which attracts more visitors, providing powerful servers at an \r\n                                            affordable price.\r\n                                        </td>\r\n                                        <td class="text-center text-wrap">\r\n                                            Great for larger websites and web applications which attracts more visitors, you wont hit any\r\n                                            limitations with this tier.\r\n                                        </td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row">24-Month Contract</th>\r\n                                        <td class="text-center text-wrap align-middle">£65 /mo</td>\r\n                                        <td class="text-center text-wrap align-middle">£130 /mo</td>\r\n                                        <td class="text-center text-wrap align-middle">£290 /mo</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row">18-Month Contract</th>\r\n                                        <td class="text-center text-wrap align-middle">£70 /mo</td>\r\n                                        <td class="text-center text-wrap align-middle">£140 /mo</td>\r\n                                        <td class="text-center text-wrap align-middle">£310 /mo</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row">12-Month Contract</th>\r\n                                        <td class="text-center text-wrap align-middle">£75 /mo</td>\r\n                                        <td class="text-center text-wrap align-middle">£150 /mo</td>\r\n                                        <td class="text-center text-wrap align-middle">£330 /mo</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row" colspan="4" class="text-center text-wrap align-middle">Server Specifications</th>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <td colspan="4" class="text-center text-wrap align-middle">\r\n                                            We have access to servers around the world with industry leading hardware,\r\n                                            providing high speeds and stability, no matter where you are in the world. Each server \r\n                                            tier uses enterprise-level solid state drives (SSD) for increased performance. Each client will recieve a private\r\n                                            server which will be dedicated to serve only your website, we do not share resources with multiple websites.\r\n                                        </td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row">CPU</th>\r\n                                        <td class="text-center text-wrap align-middle">1 Core</td>\r\n                                        <td class="text-center text-wrap align-middle">2 Cores</td>\r\n                                        <td class="text-center text-wrap align-middle">4 Cores</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row">RAM</th>\r\n                                        <td class="text-center text-wrap align-middle">1 GB</td>\r\n                                        <td class="text-center text-wrap align-middle">2 GB</td>\r\n                                        <td class="text-center text-wrap align-middle">8 GB</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row">Storage</th>\r\n                                        <td class="text-center text-wrap align-middle">20 GB SSD</td>\r\n                                        <td class="text-center text-wrap align-middle">50 GB SSD</td>\r\n                                        <td class="text-center text-wrap align-middle">150 GB SSD</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row">Bandwidth</th>\r\n                                        <td class="text-center text-wrap align-middle">1000 GB</td>\r\n                                        <td class="text-center text-wrap align-middle">3000 GB</td>\r\n                                        <td class="text-center text-wrap align-middle">5000 GB</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row" colspan="4" class="text-center text-wrap align-middle">Included Support</th>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <td colspan="4" class="text-center text-wrap align-middle">\r\n                                            Each tier has its own additional services, each service is executed by one of our engineers. Our servers \r\n                                            and each website are monitored 24/7 throughout the year to ensure your websites are running smoothly, \r\n                                            and are backed up regularly. We take pride in our efforts of ensuring safety, we regularly check for and update \r\n                                            outdated softwares, we make low-level updates to code to eliminate security vulnerabilities and we provide \r\n                                            every client with their own SSL certificates.\r\n                                        </td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row">Uptime Monitoring</th>\r\n                                        <td class="text-center text-wrap align-middle">24/7</td>\r\n                                        <td class="text-center text-wrap align-middle">24/7</td>\r\n                                        <td class="text-center text-wrap align-middle">24/7</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row">Backups</th>\r\n                                        <td class="text-center text-wrap align-middle">Weekly</td>\r\n                                        <td class="text-center text-wrap align-middle">Weekly</td>\r\n                                        <td class="text-center text-wrap align-middle">Weekly</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row">SSL Certificates</th>\r\n                                        <td class="text-center text-wrap align-middle">Included</td>\r\n                                        <td class="text-center text-wrap align-middle">Included</td>\r\n                                        <td class="text-center text-wrap align-middle">Included</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row">Security Checks</th>\r\n                                        <td class="text-center text-wrap align-middle">Weekly</td>\r\n                                        <td class="text-center text-wrap align-middle">Weekly</td>\r\n                                        <td class="text-center text-wrap align-middle">Weekly</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <td scope="row" data-bs-toggle="collapse">\r\n                                            <b>Cloudflare Content Delivery Network (CDN)</b>\r\n                                            <br>\r\n                                            <a class="btn btn-outline-primary btn-sm" data-bs-toggle="collapse" role="button" aria-expanded="false" aria-controls="collapseExample" href="#cdnHelp">What is this?</a>\r\n                                            <div class="collapse" id="cdnHelp">\r\n                                                <div class="card card-body">\r\n                                                    <p class="fs-6">\r\n                                                        Every website we host for our clients are part of the Cloudflare network, not only do you get features such as DDoS protection, you also get access to Cloudflare CDN.\r\n                                                        Cloudflare stores a copy of your website assets such as images on to many of their datacentres around the world. When a visitor accesses your website, the datacentre closest\r\n                                                        to them serves the webpages, resulting in a lightning-fast page load time.\r\n                                                    </p>\r\n                                                </div>\r\n                                            </div>\r\n                                        </td>\r\n                                        <td class="text-center text-wrap align-middle">Included</td>\r\n                                        <td class="text-center text-wrap align-middle">Included</td>\r\n                                        <td class="text-center text-wrap align-middle">Included</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <td scope="row" data-bs-toggle="collapse">\r\n                                            <b>Cloudflare DDoS Protection</b>\r\n                                            <br>\r\n                                            <a class="btn btn-outline-primary btn-sm" data-bs-toggle="collapse" role="button" aria-expanded="false" aria-controls="collapseExample" href="#ddosHelp">What is this?</a>\r\n                                            <div class="collapse" id="ddosHelp">\r\n                                                <div class="card card-body">\r\n                                                    <p class="fs-6">\r\n                                                        We use Cloudflare to detect and block hackers and other malicious visitors. Cloudflare\'s enterprise level DDoS mitigation network spans across the globe with multiple\r\n                                                        datacentres in every city, ensuring your website and website visitors are protected.\r\n                                                    </p>\r\n                                                </div>\r\n                                            </div>\r\n                                        </td>\r\n                                        <td class="text-center text-wrap align-middle">Included</td>\r\n                                        <td class="text-center text-wrap align-middle">Included</td>\r\n                                        <td class="text-center text-wrap align-middle">Included</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <td scope="row" data-bs-toggle="collapse">\r\n                                            <b>Cloudflare Code Minifier</b>\r\n                                            <br>\r\n                                            <a class="btn btn-outline-primary btn-sm" data-bs-toggle="collapse" role="button" aria-expanded="false" aria-controls="collapseExample" href="#minifyHelp">What is this?</a>\r\n                                            <div class="collapse" id="minifyHelp">\r\n                                                <div class="card card-body">\r\n                                                    <p class="fs-6">Cloudflare minify removes unnecessary characters from your source code (like whitespace, comments, etc.) without changing its functionality.\r\n                                                        Minification can compress source file size which reduces the amount of data that needs to be transferred to visitors and thus improves page load times.\r\n                                                    </p>\r\n                                                </div>\r\n                                            </div>\r\n                                        </td>\r\n                                        <td class="text-center text-wrap align-middle">-</td>\r\n                                        <td class="text-center text-wrap align-middle">Included</td>\r\n                                        <td class="text-center text-wrap align-middle">Included</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <td scope="row" data-bs-toggle="collapse">\r\n                                            <b>Cloudflare Rocket Loader™</b>\r\n                                            <br>\r\n                                            <a class="btn btn-outline-primary btn-sm" data-bs-toggle="collapse" role="button" aria-expanded="false" aria-controls="collapseExample" href="#rocketloaderHelp">What is this?</a>\r\n                                            <div class="collapse" id="rocketloaderHelp">\r\n                                                <div class="card card-body">\r\n                                                    <p class="fs-6">Javascript is one of the biggest reasons for a slow website, Cloudflare\'s Rocket Loader™ vastly optimises Javascript to exponentially increase\r\n                                                        webpage loading speeds. Visitors will have a better experience by seeing content load faster and speed is also a factor in most search engine rankings.</p>\r\n                                                </div>\r\n                                            </div>\r\n                                        </td>\r\n                                        <td class="text-center text-wrap align-middle">-</td>\r\n                                        <td class="text-center text-wrap align-middle">Included</td>\r\n                                        <td class="text-center text-wrap align-middle">Included</td>\r\n                                    </tr>\r\n                                    <tr>\r\n                                        <th scope="row">Support</th>\r\n                                        <td class="text-center text-wrap align-middle">Email + Bespoke Documentation</td>\r\n                                        <td class="text-center text-wrap align-middle">Priority Email + Bespoke Documentation</td>\r\n                                        <td class="text-center text-wrap align-middle">Priority Email + Bespoke Documentation</td>\r\n                                    </tr>\r\n                                </tbody>\r\n                            </table>', 'Hosting'), ('ewf', 'not ds')], label='Choose from the list of available pricing tables.', required=False))])), ('body_timeline_card', wagtail.core.blocks.StructBlock([('events', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Add an image.', required=False)), ('title', blocks.fields.HeadingVariableBlock(help_text="Add some text for the event card's title.", label='Card title', required=False)), ('text', blocks.fields.BodyParagraphBlock(help_text="Add some text for the event card's body.", label='Card body', required=False)), ('animated', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Select to animate on scroll.', null=True, required=False))])))]))], blank=True, help_text='Choose blocks to be shown in the body.', null=True),
        ),
    ]
