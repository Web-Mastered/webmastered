from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.db.models.fields import related
from django.utils.html import format_html

from wagtail.users.models import UserProfile

import django_tables2 as tables

from .models import Staff, Client, HostingUpgradeRequest, DNSRecordRequest, FeatureRequests, PrioritySupportSubmissions

class CustomStaffSettingsForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ["user"]

class HostingUpgradesRequestForm(forms.ModelForm):
    class Meta:
        model = HostingUpgradeRequest
        fields = "__all__"
        widgets = {
            'client': forms.HiddenInput(),
            'is_finished': forms.HiddenInput(),
            'scheduled_time': forms.HiddenInput(),
            'requested_tier': forms.Select(attrs={'class':'form-control'}),
            'client_comments': forms.Textarea(),
            'scheduled_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }
    def __init__(self, *args, **kws):
        self.user = kws.pop('user')
        super().__init__(*args, **kws)
        self.fields['client'].initial = self.user
        self.fields['is_finished'].initial = False
        self.fields['client_comments'].label = "Comments"



class DNSRecordRequestForm(forms.ModelForm):
    class Meta:
        model = DNSRecordRequest
        fields = "__all__"
        widgets = {
            'id': forms.HiddenInput(),
            'client': forms.HiddenInput(),
            'record': forms.Select(attrs={'class':'form-control'}),
            'hostname': forms.TextInput(),
            'content': forms.Textarea(),
            'ttl': forms.NumberInput(),
            'priority': forms.NumberInput(),
            'added': forms.HiddenInput(),
            'added_timestamp': forms.HiddenInput(),
        }
    def __init__(self, *args, **kws):
        form_dns_record_types = [
            ('A', 'A Record'),
            ('AAAA', 'AAAA Record'),
            ('CNAME', 'CNAME Record'),
            ('MX', 'MX Record'),
            ('TXT', 'TXT Record'),
        ]
        self.user = kws.pop('user')
        super().__init__(*args, **kws)
        self.fields['client'].initial = self.user
        self.fields['added'].initial = False
        self.fields['added_timestamp'].initial = None
        self.fields['record'].choices = form_dns_record_types

class DNSRecordRequestTable(tables.Table):
    class Meta:
        model = DNSRecordRequest
        attrs = {"id": "DNSRecordRequestDataTable"}
        row_attrs = {'data-href': lambda record: "?edit=" + str(record.get_id())}
        exclude = ("client", )



class FeatureRequestsForm(forms.ModelForm):
    class Meta:
        model = FeatureRequests
        fields = "__all__"
        widgets = {
            'id': forms.HiddenInput(),
            'client': forms.HiddenInput(),
            'feature': forms.Textarea(),
        }
    def __init__(self, *args, **kws):
        self.user = kws.pop('user')
        super().__init__(*args, **kws)
        self.fields['client'].initial = self.user

class FeatureRequestsTable(tables.Table):

    def render_feature(self, value, record):
        if len(str(value)) >= 250:
            return format_html("{}", str(value)[:250] + "...")
        else:
            return format_html("{}", str(value))
        
    class Meta:
        model = FeatureRequests
        attrs = {"id": "FeatureRequestDataTable"}
        row_attrs = {'data-href': lambda record: "?edit=" + str(record.get_id())}
        exclude = ("client", )


class PrioritySupportSubmissionsForm(forms.ModelForm):
    class Meta:
        model = PrioritySupportSubmissions
        fields = "__all__"
        widgets = {
            'id': forms.HiddenInput(),
            'client': forms.HiddenInput(),
            'message': forms.Textarea(),
        }
    def __init__(self, *args, **kws):
        self.user = kws.pop('user')
        super().__init__(*args, **kws)
        self.fields['client'].initial = self.user

class PrioritySupportSubmissionsTable(tables.Table):

    def render_message(self, value, record):
        if len(str(value)) >= 250:
            return format_html("{}", str(value)[:250] + "...")
        else:
            return format_html("{}", str(value))
        
    class Meta:
        model = PrioritySupportSubmissions
        attrs = {"id": "PrioritySupportSubmissionsDataTable"}
        row_attrs = {'data-href': lambda record: "?edit=" + str(record.get_id())}
        exclude = ("client", )