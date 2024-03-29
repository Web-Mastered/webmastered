from wagtail.core import hooks
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import BlockElementHandler
from django.utils.text import slugify
from wagtail.core.rich_text import RichText
import re

@hooks.register('register_rich_text_features')
def register_lead_feature(features):
    """
    Registering the `lead` feature.
    https://getbootstrap.com/docs/5.0/content/typography/#lead
    """
    feature_name = "lead"
    type_ = 'LEAD'

    control = {
        'type': type_,
        'label': 'Lead',
        'description': 'Make a paragraph stand out by adding lead.',
        # Optionally, we can tell Draftail what element to use when displaying those blocks in the editor.
        'element': 'p',
    }

    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.BlockFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {'p[class=lead]': BlockElementHandler(type_)},
        'to_database_format': {'block_map': {type_: {'element': 'p', 'props': {'class': 'lead'}}}},
    })


# We'll be wrapping the original RichText.__html__(), so make
# sure we have a reference to it that we can call.
__original__html__ = RichText.__html__

# This matches an h1/.../h6, using a regexp that is only
# guaranteed to work because we know that the source of
# the HTML code we'll be working with generates nice
# and predictable HTML code (and note the non-greedy
# "one or more" for the heading content).
heading_re = r"<h([1-6])([^>]*)>(.+?)</h\1>"


def add_id_attribute(match):
    """
    This is a regexp replacement function that takes
    in the above regex match results, and then turns:
        <h1>some text</h1>
    Into:
        <h1><a id="some-text"></a><a href="#some-text">some text</a></h1>
    where the id attribute value is generated by running
    the heading text through Django's slugify() function.
    """
    n = match.group(1)
    attributes= match.group(2)
    text_content = match.group(3)
    id = slugify(text_content)
    return f'<a id="{id}" class="heading-anchor-target"></a><h{n}{attributes}>{text_content}</h{n}>'


def with_heading_ids(self):
    """
    We don't actually change how RichText.__html__ works, we just replace
    it with a function that does "whatever it already did", plus a
    substitution pass that adds fragment ids and their associated link
    elements to any headings that might be in the rich text content.
    """
    html = __original__html__(self)
    return re.sub(heading_re, add_id_attribute, html)


# Rebind the RichText's html serialization function such that
# the output is still entirely functional as far as wagtail
# can tell, except with headings enriched with fragment ids.
RichText.__html__ = with_heading_ids