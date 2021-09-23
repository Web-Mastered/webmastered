from math import trunc
from CloudFlare.api_v4 import zones
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.contrib.auth.models import User

import ast
import CloudFlare
import stripe
import digitalocean
import plotly.express as px
import plotly
import pandas as pd
import pycountry
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from sentry_sdk import capture_exception
from oauth2_provider.decorators import protected_resource
import json

from .models import Client, DNSRecordRequest, Staff, HostingUpgradeRequest, FeatureRequests, PrioritySupportSubmissions, PricingTable
from .forms import HostingUpgradesRequestForm, DNSRecordRequestForm, DNSRecordRequestTable, FeatureRequestsForm, FeatureRequestsTable, PrioritySupportSubmissionsForm, PrioritySupportSubmissionsTable

def country_alpha2_to_name(alpha2):
    try:
        return pycountry.countries.get(alpha_2=alpha2).name
    except:
        return "Unknown"

def country_name_to_alpha3(name):
    try:
        return pycountry.countries.get(name=name).alpha_3
    except:
        return "Unknown"

def is_staff(thisUser):
    if Staff.objects.filter(user=thisUser):
        return True
    return False

def is_client(thisUser):
    if Client.objects.filter(user=thisUser):
        return True
    return False

def get_client(thisUser):
    thisClient = Client.objects.get(user=thisUser)
    return thisClient

@login_required(login_url='/portal/login')
def overview(request):
    thisUser = request.user

    if not is_client(thisUser):
        messages.error(request, "You cannot access the client portal as you are not a client. If this is a mistake, please contact the WM team.")
        if is_staff(thisUser):
            messages.warning(request, "You have been redirected to the admin portal as you are staff")
            return redirect('/admin')
        return redirect('/')
    else:
        thisClient = get_client(thisUser)

    template = loader.get_template('portal/pages/overview.html')

    context = {
        'page_title': "Overview",
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/portal/login')
def billing(request):
    thisUser = request.user

    if not is_client(thisUser):
        messages.error(request, "You cannot access the client portal as you are not a client. If this is a mistake, please contact the WM team.")
        if is_staff(thisUser):
            messages.warning(request, "You have been redirected to the admin portal as you are staff")
            return redirect('/admin')
        return redirect('/')
    else:
        thisClient = get_client(thisUser)

    template = loader.get_template('portal/pages/billing.html')

    context = {
        'page_title': "Billing",
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/portal/login')
def stripe_customer_portal(request):
    thisUser = request.user

    if not is_client(thisUser):
        messages.error(request, "You cannot access the client portal as you are not a client. If this is a mistake, please contact the WM team.")
        if is_staff(thisUser):
            messages.warning(request, "You have been redirected to the admin portal as you are staff")
            return redirect('/admin')
        return redirect('/')
    else:
        thisClient = get_client(thisUser)

    stripe.api_key = settings.STRIPE_API_KEY
    stripe_customer_id = thisClient.stripe_customer_id

    returnPath = str(request.build_absolute_uri()).replace('/stripe', '')

    try:
        session = stripe.billing_portal.Session.create(
            customer=str(stripe_customer_id),
            return_url=returnPath
        )
        return redirect(session.url)
    except Exception as e:
        capture_exception(e)
        template = loader.get_template('portal/pages/billing-error.html')
        context = {
            'page_title': "Billing",
        }
        return HttpResponse(template.render(context, request))


@login_required(login_url='/portal/login')
def website_metrics(request):
    thisUser = request.user

    if not is_client(thisUser):
        messages.error(request, "You cannot access the client portal as you are not a client. If this is a mistake, please contact the WM team.")
        if is_staff(thisUser):
            messages.warning(request, "You have been redirected to the admin portal as you are staff")
            return redirect('/admin')
        return redirect('/')
    else:
        thisClient = get_client(thisUser)

    today_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d').date()
    min_date = today_date - timedelta(days=2.5)

    try:
        dateParameter = str(request.GET.get('date'))
        if dateParameter == "None":
            dateParameter = today_date
        date = datetime.strptime(str(dateParameter), '%Y-%m-%d').date()
        if not min_date <= date <= today_date:
            raise ValueError('Input date is outside of boundary.')
    except ValueError as e:
        date = today_date
        messages.error(request, "Invalid date entered! Showing metrics with today's date instead.")

    cf_graphql = CloudFlare.CloudFlare(
        email=settings.CLOUDFLARE_EMAIL,
        token=settings.CLOUDFLARE_ORIGIN_API_TOKEN
    )

    query = """
{
  viewer {
    zones(filter: {zoneTag: "%s"}) {
      firewallEventsAdaptive(limit: 10000, filter: {date: "%s"}) {
        action
        clientCountryName
        clientAsn
        clientASNDescription
        clientIP
        clientRequestScheme
        clientRequestHTTPHost
        datetime
        userAgent
      }
      httpRequests1dGroups(limit: 10000, filter:{date: "%s"}) {
        sum {
          threats
          requests
          pageViews
          countryMap {
            clientCountryName
            requests
            threats
            bytes
          }
          
          browserMap {
            pageViews
            uaBrowserFamily
          }
        }
        dimensions {
          date
        }
        uniq {
          uniques
        }
      }
      httpRequests1hGroups(
        limit: 25, 
        filter: {date: "%s"}, 
        orderBy: [datetime_ASC]
      ) {
        avg {
          bytes
        }
        dimensions {
          datetime
        }
        sum {
          requests
          cachedRequests
          encryptedRequests
          bytes
          cachedBytes
          encryptedBytes
          pageViews
          threats
        }
        uniq {
          uniques
        }
      }
    }
  }
}
    """%(thisClient.cloudflare_zone_id, date, date, date)

    apiError = None
    try:
        r = cf_graphql.graphql.post(data={'query':query})
        zone_info = r['data']['viewer']['zones'][0]
        httpRequests1dGroups = zone_info['httpRequests1dGroups']
        httpRequests1hGroups = zone_info['httpRequests1hGroups']
        firewallEventsAdaptive = zone_info['firewallEventsAdaptive']

        page_views = int(httpRequests1dGroups[0]['sum']['pageViews'])
        total_threats = int(httpRequests1dGroups[0]['sum']['threats'])
        total_requests = int(httpRequests1dGroups[0]['sum']['requests'])
        unique_visitors = int(httpRequests1dGroups[0]['uniq']['uniques'])

        CountryRequests24hDataDict = httpRequests1dGroups[0]['sum']['countryMap']

        BrowserMap24hDataDict = httpRequests1dGroups[0]['sum']['browserMap']

        HourlyRequestDataList = []
        for thisHour in httpRequests1hGroups:
            data = {
                "Timestamp (Zulu/UTC)" : datetime.strptime(thisHour['dimensions']['datetime'], '%Y-%m-%dT%H:%M:%SZ').time(),
                "Requests" : thisHour['sum']['requests'],
                "Page Views" : thisHour['sum']['pageViews'],
                "Threats" : thisHour['sum']['threats'],
                "Bytes Transferred" : thisHour['sum']['bytes'],
            }
            HourlyRequestDataList.append(data)

        FirewallEventsDataList = []
        for firewallEvent in firewallEventsAdaptive:
            data = {
                "Timestamp (Zulu/UTC)" : datetime.strptime(firewallEvent['datetime'], '%Y-%m-%dT%H:%M:%SZ').time(),
                "Client Location" : country_alpha2_to_name(firewallEvent['clientCountryName']),
                "Client IP" : firewallEvent['clientIP'],
                "Client Description" : firewallEvent['clientASNDescription'],
                "Client User Agent" : firewallEvent['userAgent'],
                "Firewall Action" : firewallEvent['action'],
            }
            FirewallEventsDataList.append(data)

        HourlyRequestDataFrame = pd.DataFrame(HourlyRequestDataList, columns=['Timestamp (Zulu/UTC)', 'Requests', 'Page Views', 'Threats', 'Bytes Transferred'])
        FirewallEventsDataFrame = pd.DataFrame(FirewallEventsDataList, columns=['Timestamp (Zulu/UTC)', 'Client IP', 'Client Description', 'Client User Agent', 'Firewall Action'])

        CountryRequests24hDataFrame = pd.DataFrame(CountryRequests24hDataDict).reindex(columns=['clientCountryName','requests','threats', 'bytes'])
        CountryRequests24hDataFrame['clientCountryName'] = CountryRequests24hDataFrame['clientCountryName'].apply(country_alpha2_to_name)
        CountryRequests24hDataFrame = CountryRequests24hDataFrame.rename(columns={
            'clientCountryName': 'Country Name',
            'requests' : 'Requests',
            'threats' : 'Threats',
            'bytes' : 'Bytes'
            }
        )

        BrowserMap24hDataFrame = pd.DataFrame(BrowserMap24hDataDict).reindex(columns=['pageViews','uaBrowserFamily'])
        BrowserMap24hDataFrame = BrowserMap24hDataFrame.rename(columns={
            'pageViews': 'Page Views',
            'uaBrowserFamily' : 'Browser Family'
            }
        )

        CountryRequests24hDataFrame['Country Code'] = CountryRequests24hDataFrame['Country Name'] 
        CountryRequests24hDataFrame['Country Code'] = CountryRequests24hDataFrame['Country Code'].apply(country_name_to_alpha3)

        CountryRequests24hDataFrame = CountryRequests24hDataFrame[['Country Name', 'Country Code', 'Requests', 'Threats', 'Bytes']]
        BrowserMap24hDataFrame = BrowserMap24hDataFrame[['Browser Family', 'Page Views']]

        BrowserRequest24hHTMLTable = CountryRequests24hDataFrame.to_html(classes = 'BrowserRequest24hDataTable custom-data-table stripe" id = "BrowserRequest24hDataTable', index=False)
        HourlyRequestHTMLTable = HourlyRequestDataFrame.to_html(classes = 'HourlyRequestDataTable custom-data-table stripe" id = "HourlyRequestDataTable', index=False)
        FirewallEventsHTMLTable = FirewallEventsDataFrame.to_html(classes = 'FirewallEventsDataTable custom-data-table stripe" id = "FirewallEventsDataTable', index=False)
        BrowserMap24hHTMLTable = BrowserMap24hDataFrame.to_html(classes = 'BrowserMap24hDataTable custom-data-table stripe" id = "BrowserMap24hDataTable', index=False)

        CountryRequests24h = px.choropleth(
            CountryRequests24hDataFrame,
            locationmode='ISO-3',
            locations = 'Country Code',
            color='Requests',
            hover_name="Country Name",
            hover_data = {
                'Country Name' : False,
                'Country Code' : True,
                'Requests' : True,
                'Threats' : True,
                'Bytes' : True
            },
            color_continuous_scale=px.colors.sequential.Oranges,
        )

        CountryRequests24hConfig = {
            'responsive': True,
            'displaylogo': False
        }

        CountryRequests24hHTMLMap = plotly.io.to_html(CountryRequests24h, config=CountryRequests24hConfig)

    except CloudFlare.exceptions.CloudFlareAPIError as e:
        apiError = """
        An error occurred when fetching the website metrics.
        Please try again later, contact the WM engineers if this error continues.
        We apologise for the inconvenience.
        """
        print('/graphql.post %d %s - api call failed' % (e, e))
        
    if apiError == None:
        context = {
            'page_title': "Website Metrics",
            "error": apiError,
            'metrics_date_display': date,
            'metrics_datepicker_value': date.strftime('%Y-%m-%d'),
            'max_metrics_date': today_date.strftime('%Y-%m-%d'),
            'min_metrics_date': min_date.strftime('%Y-%m-%d'),
            'page_views': page_views,
            'unique_visitors': unique_visitors,
            'total_requests': total_requests,
            'total_threats': total_threats,
            'country_requests_24h_map': CountryRequests24hHTMLMap,
            'browser_requests_24h_table' : BrowserRequest24hHTMLTable,
            'hourly_requests_table' : HourlyRequestHTMLTable,
            'browser_map_table' : BrowserMap24hHTMLTable,
            'firewall_events_table': FirewallEventsHTMLTable,
        }
    else:
        context = {
            'page_title': "Website Metrics",
            "error": apiError,
            'metrics_date_display': None,
            'metrics_datepicker_value': None,
            'max_metrics_date': None,
            'min_metrics_date': None,
            'page_views': None,
            'unique_visitors': None,
            'total_requests': None,
            'total_threats': None,
            'country_requests_24h_map': None,
            'browser_requests_24h_table' : None,
            'hourly_requests_table' : None,
            'browser_map_table' : None,
            'firewall_events_table': None,
        }

    template = loader.get_template('portal/pages/website-metrics.html')
    return HttpResponse(template.render(context, request))


@login_required(login_url='/portal/login')
def server_metrics(request):
    thisUser = request.user

    if not is_client(thisUser):
        messages.error(request, "You cannot access the client portal as you are not a client. If this is a mistake, please contact the WM team.")
        if is_staff(thisUser):
            messages.warning(request, "You have been redirected to the admin portal as you are staff")
            return redirect('/admin')
        return redirect('/')
    else:
        thisClient = get_client(thisUser)

    do_error = None
    try:
        do_manager = digitalocean.Manager(token=settings.DIGITALOCEAN_ACCESS_TOKEN)
        do_droplet = do_manager.get_droplet(droplet_id=thisClient.digitalocean_droplet_id)
    except Exception as e:
        do_error = """
        An error occurred when fetching the server metrics.
        Please try again later, contact the WM engineers if this error continues.
        We apologise for the inconvenience.
        """

    droplet_cpu_count = do_droplet.vcpus
    droplet_ram_total = trunc(do_droplet.memory/1024)
    droplet_disk_total = do_droplet.disk
    droplet_status = do_droplet.status

    try:
        headers = {'User-Agent': 'WM Telemetry Services (WM Engine / Client Portal)'}
        wm_engine_metrics_url = "https://" + thisClient.domain_name + "/wm-engine-metrics/"
        wm_engine_metrics_request = Request(url=wm_engine_metrics_url, headers=headers)
        wm_engine_metrics = urlopen(wm_engine_metrics_request).read()
        wm_engine_metrics = wm_engine_metrics.decode("UTF-8")
        wm_engine_metrics = ast.literal_eval(wm_engine_metrics)
    except Exception as e:
        do_error = """
        An error occurred when fetching the server metrics.
        Please try again later, contact the WM engineers if this error continues.
        We apologise for the inconvenience.
        """
        template = loader.get_template('portal/pages/server-metrics.html')
        context = {
            'page_title': "Server Metrics",
            'error': do_error,
        }
        return HttpResponse(template.render(context, request))

    template = loader.get_template('portal/pages/server-metrics.html')

    context = {
        'page_title': "Server Metrics",
        'error': do_error,
        'cpu_count': droplet_cpu_count,
        'ram_total': droplet_ram_total,
        'disk_total': droplet_disk_total,
        'status': droplet_status,
        'cpu_data': wm_engine_metrics["cpu"],
        'ram_data': wm_engine_metrics["ram"],
        'ram_total_bytes': wm_engine_metrics["ram"]["total"],
        'ram_total_gigabytes': round(wm_engine_metrics["ram"]["total"]/1024/1024/1024,2),
        'ram_avail_bytes': wm_engine_metrics["ram"]["avail"],
        'ram_avail_gigabytes': round(wm_engine_metrics["ram"]["avail"]/1024/1024/1024,2),
        'ram_used_bytes': wm_engine_metrics["ram"]["used"],
        'ram_used_gigabytes': round(wm_engine_metrics["ram"]["used"]/1024/1024/1024,2),
        'disk_data': wm_engine_metrics["disk"],
        'disk_total_bytes': wm_engine_metrics["disk"]["total"],
        'disk_total_gigabytes': round(wm_engine_metrics["disk"]["total"]/1024/1024/1024,2),
        'disk_avail_bytes': wm_engine_metrics["disk"]["avail"],
        'disk_avail_gigabytes': round(wm_engine_metrics["disk"]["avail"]/1024/1024/1024,2),
        'disk_used_bytes': wm_engine_metrics["disk"]["used"],
        'disk_used_gigabytes': round(wm_engine_metrics["disk"]["used"]/1024/1024/1024,2),
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/portal/login')
def upgrades(request):
    thisUser = request.user

    if not is_client(thisUser):
        messages.error(request, "You cannot access the client portal as you are not a client. If this is a mistake, please contact the WM team.")
        if is_staff(thisUser):
            messages.warning(request, "You have been redirected to the admin portal as you are staff")
            return redirect('/admin')
        return redirect('/')
    else:
        thisClient = get_client(thisUser)

    for table in PricingTable.objects.all():
        if table.hosting_prices:
            table_html = table.html_table
        else:
            table_html = """
            ERROR! Couldn't find hosting pricing table! Please report this to the WM team.
            """

    form_exists = False
    if request.method == 'POST':
        if HostingUpgradeRequest.objects.filter(client=thisClient).exists():
            existing_form_instance = HostingUpgradeRequest.objects.get(client=thisClient)
            upgrade_form = HostingUpgradesRequestForm(request.POST, user=thisClient, instance=existing_form_instance)
        else:
            upgrade_form = HostingUpgradesRequestForm(request.POST, user=thisClient)
        if upgrade_form.is_valid():
            upgrade_form.save()
            messages.success(request, "Your upgrade request has been sent, we will get back to you soon.")
            return redirect("/portal/upgrades")
    else:
        if HostingUpgradeRequest.objects.filter(client=thisClient).exists():
            existing_form_instance = HostingUpgradeRequest.objects.get(client=thisClient)
            upgrade_form = HostingUpgradesRequestForm(user=thisClient, instance=existing_form_instance)
            form_exists = True
        else:
            upgrade_form = HostingUpgradesRequestForm(user=thisClient)

    template = loader.get_template('portal/pages/upgrades.html')

    context = {
        'page_title': "Upgrades",
        'pricing_table': table_html,
        'upgrade_form': upgrade_form,
        'form_exists': form_exists,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/portal/login')
def dns_records(request):
    thisUser = request.user

    if not is_client(thisUser):
        messages.error(request, "You cannot access the client portal as you are not a client. If this is a mistake, please contact the WM team.")
        if is_staff(thisUser):
            messages.warning(request, "You have been redirected to the admin portal as you are staff")
            return redirect('/admin')
        return redirect('/')
    else:
        thisClient = get_client(thisUser)

    editting = False

    edit_id = request.GET.get("edit")
    delete_id = request.GET.get("delete")
    if request.method == 'POST':
        if edit_id:
            existing_form_instance = DNSRecordRequest.objects.get(id=edit_id, client=thisClient)
            post = request.POST.copy()
            post['added'] = False
            post['added_timestamp'] = None
            dns_form = DNSRecordRequestForm(post, user=thisClient, instance=existing_form_instance)
        else:
            dns_form = DNSRecordRequestForm(request.POST, user=thisClient)
        if dns_form.is_valid():
            dns_form.save()
            messages.success(request, "Your DNS record submission has been sent, we will add this as soon as possible.")
            return redirect("/portal/dns-records")
    else:
        if edit_id:
            editting = True
            existing_form_instance = DNSRecordRequest.objects.get(id=edit_id, client=thisClient)
            dns_form = DNSRecordRequestForm(user=thisClient, instance=existing_form_instance)
        else:
            if delete_id:
                DNSRecordRequest.objects.filter(id=delete_id, client=thisClient).delete()
                messages.success(request, "Your DNS record submission has been deleted, we will remove it from the DNS system as soon as possible.")
                dns_form = DNSRecordRequestForm(user=thisClient)
                return redirect("/portal/dns-records")
            else:
                dns_form = DNSRecordRequestForm(user=thisClient)

    queryset = DNSRecordRequest.objects.filter(client=thisClient)
    dns_table = DNSRecordRequestTable(queryset)

    if queryset.exists():
        table_populated = True
    else:
        table_populated = False

    template = loader.get_template('portal/pages/dns-records.html')

    context = {
        'page_title': "DNS Records",
        'editting': editting,
        'dns_form': dns_form,
        'dns_table': dns_table,
        'edit_id': edit_id,
        'table_populated': table_populated,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/portal/login')
def add_features(request):
    thisUser = request.user

    if not is_client(thisUser):
        messages.error(request, "You cannot access the client portal as you are not a client. If this is a mistake, please contact the WM team.")
        if is_staff(thisUser):
            messages.warning(request, "You have been redirected to the admin portal as you are staff")
            return redirect('/admin')
        return redirect('/')
    else:
        thisClient = get_client(thisUser)

    editting = False

    edit_id = request.GET.get("edit")
    delete_id = request.GET.get("delete")
    if request.method == 'POST':
        if edit_id:
            existing_form_instance = FeatureRequests.objects.get(id=edit_id, client=thisClient)
            feature_request_form = FeatureRequestsForm(request.POST, user=thisClient, instance=existing_form_instance)
        else:
            feature_request_form = FeatureRequestsForm(request.POST, user=thisClient)
        if feature_request_form.is_valid():
            feature_request_form.save()
            messages.success(request, "Your feature request submission has been sent, we will get back to you as soon as possible.")
            return redirect("/portal/add-features")
    else:
        if edit_id:
            editting = True
            existing_form_instance = FeatureRequests.objects.get(id=edit_id, client=thisClient)
            feature_request_form = FeatureRequestsForm(user=thisClient, instance=existing_form_instance)
        else:
            if delete_id:
                FeatureRequests.objects.filter(id=delete_id, client=thisClient).delete()
                messages.success(request, "Your feature request submission has been deleted.")
                feature_request_form = FeatureRequestsForm(user=thisClient)
                return redirect("/portal/add-features")
            else:
                feature_request_form = FeatureRequestsForm(user=thisClient)

    queryset = FeatureRequests.objects.filter(client=thisClient)
    feature_request_table = FeatureRequestsTable(queryset)

    if queryset.exists():
        table_populated = True
    else:
        table_populated = False

    template = loader.get_template('portal/pages/add-features.html')

    context = {
        'page_title': "Add Features",
        'editting': editting,
        'feature_request_form': feature_request_form,
        'feature_request_table': feature_request_table,
        'edit_id': edit_id,
        'table_populated': table_populated,
    }
    return HttpResponse(template.render(context, request))



@login_required(login_url='/portal/login')
def priority_support(request):
    thisUser = request.user

    if not is_client(thisUser):
        messages.error(request, "You cannot access the client portal as you are not a client. If this is a mistake, please contact the WM team.")
        if is_staff(thisUser):
            messages.warning(request, "You have been redirected to the admin portal as you are staff")
            return redirect('/admin')
        return redirect('/')
    else:
        thisClient = get_client(thisUser)

    editting = False

    edit_id = request.GET.get("edit")
    delete_id = request.GET.get("delete")
    if request.method == 'POST':
        if edit_id:
            existing_form_instance = PrioritySupportSubmissions.objects.get(id=edit_id, client=thisClient)
            support_request_form = PrioritySupportSubmissionsForm(request.POST, user=thisClient, instance=existing_form_instance)
        else:
            support_request_form = PrioritySupportSubmissionsForm(request.POST, user=thisClient)
        if support_request_form.is_valid():
            support_request_form.save()
            messages.success(request, "Your feature request submission has been sent, we will get back to you as soon as possible.")
            return redirect("/portal/priority-support")
    else:
        if edit_id:
            editting = True
            existing_form_instance = PrioritySupportSubmissions.objects.get(id=edit_id, client=thisClient)
            support_request_form = PrioritySupportSubmissionsForm(user=thisClient, instance=existing_form_instance)
        else:
            if delete_id:
                PrioritySupportSubmissions.objects.filter(id=delete_id, client=thisClient).delete()
                messages.success(request, "Your feature request submission has been deleted.")
                support_request_form = PrioritySupportSubmissionsForm(user=thisClient)
                return redirect("/portal/priority-support")
            else:
                support_request_form = PrioritySupportSubmissionsForm(user=thisClient)

    queryset = PrioritySupportSubmissions.objects.filter(client=thisClient)
    support_request_table = PrioritySupportSubmissionsTable(queryset)

    if queryset.exists():
        table_populated = True
    else:
        table_populated = False

    template = loader.get_template('portal/pages/priority-support.html')

    context = {
        'page_title': "Add Features",
        'editting': editting,
        'support_request_form': support_request_form,
        'support_request_table': support_request_table,
        'edit_id': edit_id,
        'table_populated': table_populated,
    }
    return HttpResponse(template.render(context, request))


@protected_resource()
def oauth_user_resource(request, *args, **kwargs):
    print(request.user)
    this_user = User.objects.get(username__iexact=request.user.username)
    print("over here")
    return HttpResponse(
        json.dumps({
            'username': this_user.username, 
            'email': this_user.email}),
        content_type='application/json')