from django import template
from dashboard.models import WebsiteSettings, Contact, SocialMediaAccount, LinkedURL
from django.conf import settings
import json
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def render_organisation_schema(context):
    request = context['request']
    website_settings = WebsiteSettings.for_request(request)

    legalName = website_settings.organisation_legal_name
    name = website_settings.organisation_alternate_name
    alternateName = name
    url = settings.BASE_URL
    logo = url + website_settings.logo.file.url
    
    contactPoint = []
    for contact in Contact.objects.all():
        contactPoint_dict = {
            "@type" : "contactPoint",
            "contactType": contact.contact_type,
            "email": contact.email
        }

        if contact.telephone:
            contactPoint_dict["telephone"] = contact.telephone

        contactPoint.append(contactPoint_dict)

    sameAs = []
    for account in SocialMediaAccount.objects.all():
        sameAs.append(account.account_url)
    for link in LinkedURL.objects.all():
        sameAs.append(link.link)

    json_string = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "legalName": legalName,
        "name": name,
        "alternateName": alternateName,
        "url": url,
        "logo": logo,
        "contactPoint": contactPoint,
        "sameAs": sameAs
    }

    render_string = '<script type="application/ld+json">\n' + str(json.dumps(json_string, sort_keys=True, indent=4)) + '\n</script>'

    return mark_safe(render_string)
