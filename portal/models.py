from django.db import models
from django.contrib.auth.models import User
from django.db.models import fields
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
from django.forms import ModelForm
from django.contrib import messages
from django.http import request
from django.template.defaultfilters import first
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from wagtail.core import hooks


class StaffRoles(models.Model):
    role = models.CharField(max_length=154, unique=True, help_text="Create new staff roles here, these roles an be assigned to 'staff' users.")
    panels = [
        FieldPanel('role'),
    ]

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = "Staff Role"
        verbose_name_plural = "Staff Roles"

class StaffRolesAdmin(ModelAdmin):
    model = StaffRoles
    menu_label = "Staff Roles"
    menu_icon = "group"

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    bio = models.TextField(max_length=1024, blank=True)
    roles = models.ManyToManyField(StaffRoles, blank=True)
    
    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"


class PricingTable(models.Model):
    name = models.CharField(help_text="Identifying name for this pricing table.", max_length=255, unique=True)
    hosting_prices = models.BooleanField(default=False, help_text="If this is set to true, this table will be displayed in the client portal under the server upgrades page.")
    html_table = models.TextField(max_length=500000, blank=False, help_text="HTML table for pricing.", verbose_name="HTML Table")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Pricing Table"
        verbose_name_plural = "Pricing Tables"

class PricingTableAdmin(ModelAdmin):
    model = PricingTable
    menu_label = "Pricing Tables"
    menu_icon = "table"

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    domain_name = models.CharField(help_text="Customer's website domain name.", max_length=255, unique=True)
    stripe_customer_id = models.CharField(help_text="Stripe ID of customer", max_length=255, unique=True, verbose_name="Stripe Customer ID")
    cloudflare_zone_id = models.CharField(help_text="CF Zone ID of customer", max_length=255, unique=True, verbose_name="Cloudflare Zone ID")
    digitalocean_droplet_id = models.CharField(help_text="DO Droplet ID of customer", max_length=255, unique=True, verbose_name="DigitalOcean Droplet ID")
    
    def __str__(self):
        return str(self.user.first_name) + " " + str(self.user.last_name)

    def first_name(self):
        return str(self.user.first_name)

    def last_name(self):
        return str(self.user.last_name)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

class ClientAdmin(ModelAdmin):
    model = Client
    list_display = ('first_name', 'last_name', 'domain_name', 'stripe_customer_id', 'cloudflare_zone_id', 'digitalocean_droplet_id')
    menu_label = "Clients"
    menu_icon = "user"


class HostingUpgradeRequest(models.Model):

    hosting_tiers = [
        ('Basic 12M', 'Basic 12M'),
        ('Basic 18M', 'Basic 18M'),
        ('Basic 24M', 'Basic 24M'),
        ('Standard 12M', 'Standard 12M'),
        ('Standard 18M', 'Standard 18M'),
        ('Standard 24M', 'Standard 24M'),
        ('Professional 12M', 'Professional 12M'),
        ('Professional 18M', 'Professional 18M'),
        ('Professional 24M', 'Professional 24M'),
    ]

    client = models.OneToOneField(Client, on_delete=models.CASCADE, blank=False, null=False)
    requested_tier = models.CharField(help_text="This is the hosting tier that the client wants to upgrade to.", max_length=255, verbose_name="Requested tier", choices=hosting_tiers, blank=False, null=False)
    client_comments = models.TextField(max_length=500000, blank=True, null=True, help_text="Comments left by client.", verbose_name="Client comments")
    scheduled_date = models.DateField(editable=True, help_text="Date scheduled to carry out the upgrade.", blank=True, null=True)
    scheduled_time = models.TimeField(editable=True, help_text="Scheduled time on the scheduled date when the upgrade process will start", blank=True, null=True)
    is_finished = models.BooleanField()

    def __str__(self):
        return str(self.client.user.first_name) + " " + str(self.client.user.last_name)

    def first_name(self):
        return str(self.client.user.first_name)

    def last_name(self):
        return str(self.client.user.last_name)

    def domain_name(self):
        return str(self.client.domain_name)

    def save(self, *args, **kwargs):
        super(HostingUpgradeRequest, self).save(*args, **kwargs)

        if self.is_finished:
            self.delete()
        else:
            staff = Staff.objects.all()
            emails = []
            for thisUser in staff:
                emails.append(thisUser.user.email)

            addresses = emails
            from_address = settings.DEFAULT_FROM_EMAIL
            subject = 'WM Client Hosting Upgrade Request'

            content = """
Hello WM Team,

A client named, %s, with the domain name, %s, is requesting for a hosting upgrade to the %s tier on the date, %s.

Below are the client's comments:
---
%s
---

Please prepare for this upgrade request, confirm the scheduled date and time with the client, then enter the scheduled time and date for the upgrade in the WM Admin Portal.

Best wishes,
WM Client Portal
    """%(self.first_name() + " " + self.last_name(), self.domain_name(), self.requested_tier, self.scheduled_date, self.client_comments)

            email = EmailMessage(
                subject=subject,
                body=content,
                from_email=from_address,
                to=addresses
            )

            email.send(fail_silently=True)

    class Meta:
        verbose_name = "Hosting Upgrade Request"
        verbose_name_plural = "Hosting Upgrade Requests"

class HostingUpgradeRequestAdmin(ModelAdmin):
    model = HostingUpgradeRequest
    list_display = ('first_name', 'last_name', 'domain_name', 'requested_tier', 'scheduled_date', 'scheduled_time')
    menu_label = "Upgrade Requests"
    menu_icon = "order-up"


class DNSRecordRequest(models.Model):
    dns_record_types = [
        ('A', 'A Record'),
        ('AAAA', 'AAAA Record'),
        ('CNAME', 'CNAME Record'),
        ('MX', 'MX Record'),
        ('TXT', 'TXT Record'),
        ('OTHER', 'Other Record'),
    ]

    id = models.AutoField(primary_key=True, verbose_name="ID")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False, null=False)
    record = models.CharField(help_text="Choose the type of records this is.", max_length=255, verbose_name="Type", choices=dns_record_types, blank=False, null=False)
    hostname = models.CharField(help_text="This is the hostname for the records.", max_length=255, verbose_name="Hostname", blank=False, null=False)
    content = models.CharField(help_text="This is where the hostname points to.", max_length=2048, verbose_name="Content", blank=False, null=False)
    ttl = models.IntegerField(help_text="OPTIONAL. This is the TTL of the records, this can be left blank.", blank=True, null=True, verbose_name="TTL")
    priority = models.IntegerField(help_text="ONLY FOR MX RECORDS. This is the priority of the record.", blank=True, null=True, verbose_name="MX Priority")
    added = models.BooleanField(default=False)
    added_timestamp = models.DateTimeField(editable=True, blank=True, null=True)
    
    def __str__(self):
        return str(self.client.user.first_name) + " " + str(self.client.user.last_name)

    def first_name(self):
        return str(self.client.user.first_name)

    def last_name(self):
        return str(self.client.user.last_name)

    def domain_name(self):
        return str(self.client.domain_name)

    def get_id(self):
        return str(self.id)


    class Meta:
        verbose_name = "DNS Record Request"
        verbose_name_plural = "DNS Record Requests"

class DNSRecordRequestAdmin(ModelAdmin):
    model = DNSRecordRequest
    list_display = ('id', 'first_name', 'last_name', 'domain_name', 'record', 'added')
    menu_label = "DNS Record Requests"
    menu_icon = "site"


class FeatureRequests(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False, null=False)
    feature = models.TextField(max_length=100000, blank=False, null=False)

    def first_name(self):
        return str(self.client.user.first_name)

    def last_name(self):
        return str(self.client.user.last_name)

    def get_id(self):
        return str(self.id)

    def get_feature_short(self):
        return str(self.feature)[:500] + "..."
    get_feature_short.short_description = 'Feature' 

    def domain_name(self):
        return str(self.client.domain_name)

    class Meta:
        verbose_name = "Feature Request"
        verbose_name_plural = "Feature Requests"

class FeatureRequestsAdmin(ModelAdmin):
    model = FeatureRequests
    list_display = ('id', 'first_name', 'last_name', 'get_feature_short')
    menu_label = "Feature Requests"
    menu_icon = "comment"


class PrioritySupportSubmissions(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False, null=False)
    message = models.TextField(max_length=100000, blank=False, null=False)

    def first_name(self):
        return str(self.client.user.first_name)

    def last_name(self):
        return str(self.client.user.last_name)

    def get_id(self):
        return str(self.id)

    def get_message_short(self):
        return str(self.message)[:500] + "..."
    get_message_short.short_description = 'Message' 

    def domain_name(self):
        return str(self.client.domain_name)

    class Meta:
        verbose_name = "Priority Support Submission"
        verbose_name_plural = "Priority Support Submissions"

class PrioritySupportSubmissionsAdmin(ModelAdmin):
    model = PrioritySupportSubmissions
    list_display = ('id', 'first_name', 'last_name', 'get_message_short')
    menu_label = "Priority Support Submissions"
    menu_icon = "help"


class WMBusinessAdminGroup(ModelAdminGroup):
    menu_label = 'WM Business'
    menu_icon = 'site'
    items = (StaffRolesAdmin, PricingTableAdmin, ClientAdmin, HostingUpgradeRequestAdmin, DNSRecordRequestAdmin, FeatureRequestsAdmin, PrioritySupportSubmissionsAdmin)

modeladmin_register(WMBusinessAdminGroup)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        Staff.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    pass

@receiver(post_save, sender=DNSRecordRequest)
def DNSRecordRequest_email_on_save(instance, **kwargs):
    if not instance.added:
        staff = Staff.objects.all()
        emails = []
        for thisUser in staff:
            emails.append(thisUser.user.email)

        addresses = emails
        from_address = settings.DEFAULT_FROM_EMAIL
        subject = 'WM Client DNS Record Submission NEW/ALTERED'

        content = """
Hello WM Team,

A client named, %s, with the domain name, %s, is requesting for a DNS record to be ADDED/ALTERED. You can find this submission listed in the WM Admin Portal WM Business > DNS Record Requests.

Submission ID : %s

Please prepare for this DNS record request, confirm the details with the client if needed. Add the record to Cloudflare then make sure to set "added" to True and "added timestamp" to the date and time the record was added.

Best wishes,
WM Client Portal
"""%(instance.first_name() + " " + instance.last_name(), instance.domain_name(), instance.id)

        email = EmailMessage(
            subject=subject,
            body=content,
            from_email=from_address,
            to=addresses
        )

        email.send(fail_silently=True)



@receiver(post_delete, sender=DNSRecordRequest)
def DNSRecordRequest_email_on_delete(instance, **kwargs):
    staff = Staff.objects.all()
    emails = []
    for thisUser in staff:
        emails.append(thisUser.user.email)

    addresses = emails
    from_address = settings.DEFAULT_FROM_EMAIL
    subject = 'WM Client DNS Record Submission DELETED'

    content = """
Hello WM Team,

A client named, %s, with the domain name, %s, is requesting for a DNS record to be DELETED. You can find this submission listed in the WM Admin Portal WM Business > DNS Record Requests.

Submission ID : %s
Type: %s
Hostname: %s
Content: %s
TTL: %s
MX Priority: %s

Please DELETE this DNS record from Cloudflare, confirm the details with the client if needed.

Best wishes,
WM Client Portal
"""%(instance.first_name() + " " + instance.last_name(), instance.domain_name(), instance.id, instance.record, instance.hostname, instance.content, instance.ttl, instance.priority)

    email = EmailMessage(
        subject=subject,
        body=content,
        from_email=from_address,
        to=addresses
    )

    email.send(fail_silently=True)




@receiver(post_save, sender=FeatureRequests)
def FeatureRequests_email_on_save(instance, **kwargs):
    staff = Staff.objects.all()
    emails = []
    for thisUser in staff:
        emails.append(thisUser.user.email)

    addresses = emails
    from_address = settings.DEFAULT_FROM_EMAIL
    subject = 'WM Client Feature Request Submission NEW/ALTERED'

    content = """
Hello WM Team,

A client named, %s, with the domain name, %s, is requesting for a new feature to be implemented to their website/web-app. You can find this submission listed in the WM Admin Portal WM Business > Feature Requests.

Submission ID : %s
feature: (below)
---
%s
---

Please prepare for this feature request, confirm the details with the client if needed.

Best wishes,
WM Client Portal
"""%(instance.first_name() + " " + instance.last_name(), instance.domain_name(), instance.id, instance.feature)

    email = EmailMessage(
        subject=subject,
        body=content,
        from_email=from_address,
        to=addresses
    )

    email.send(fail_silently=True)



@receiver(post_delete, sender=FeatureRequests)
def FeatureRequests_email_on_delete(instance, **kwargs):
    staff = Staff.objects.all()
    emails = []
    for thisUser in staff:
        emails.append(thisUser.user.email)

    addresses = emails
    from_address = settings.DEFAULT_FROM_EMAIL
    subject = 'WM Client Feature Request Submission DELETED'

    content = """
Hello WM Team,

A client named, %s, with the domain name, %s, has deleted their feature request submission.

deleted feature request: (below)
---
%s
---

Best wishes,
WM Client Portal
"""%(instance.first_name() + " " + instance.last_name(), instance.domain_name(), instance.feature)

    email = EmailMessage(
        subject=subject,
        body=content,
        from_email=from_address,
        to=addresses
    )

    email.send(fail_silently=True)





@receiver(post_save, sender=PrioritySupportSubmissions)
def PrioritySupportSubmissions_email_on_save(instance, **kwargs):
    staff = Staff.objects.all()
    emails = []
    for thisUser in staff:
        emails.append(thisUser.user.email)

    addresses = emails
    from_address = settings.DEFAULT_FROM_EMAIL
    subject = 'WM Client Priority Support Submission NEW/ALTERED'

    content = """
Hello WM Team,

A client named, %s, with the domain name, %s, is requesting for priority support. You can find this submission listed in the WM Admin Portal WM Business > Priority Support Submissions.

Submission ID : %s
message: (below)
---
%s
---

Please carry out the support tasks for this client.

Best wishes,
WM Client Portal
"""%(instance.first_name() + " " + instance.last_name(), instance.domain_name(), instance.id, instance.message)

    email = EmailMessage(
        subject=subject,
        body=content,
        from_email=from_address,
        to=addresses
    )

    email.send(fail_silently=True)



@receiver(post_delete, sender=PrioritySupportSubmissions)
def PrioritySupportSubmissions_email_on_delete(instance, **kwargs):
    staff = Staff.objects.all()
    emails = []
    for thisUser in staff:
        emails.append(thisUser.user.email)

    addresses = emails
    from_address = settings.DEFAULT_FROM_EMAIL
    subject = 'WM Client Priority Support Submission DELETED'

    content = """
Hello WM Team,

A client named, %s, with the domain name, %s, has deleted their priority support submission.

deleted support message: (below)
---
%s
---

Best wishes,
WM Client Portal
"""%(instance.first_name() + " " + instance.last_name(), instance.domain_name(), instance.message)

    email = EmailMessage(
        subject=subject,
        body=content,
        from_email=from_address,
        to=addresses
    )

    email.send(fail_silently=True)