from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.overview, name="portal_overview"),
    path('billing', views.billing, name="portal_billing"),
    path('billing/stripe', views.stripe_customer_portal, name="portal_billing_stripe"),
    path('website-metrics', views.website_metrics, name="portal_website_metrics"),
    path('server-metrics', views.server_metrics, name="portal_server_metrics"),
    path('upgrades', views.upgrades, name="portal_server_upgrades"),
    path('dns-records', views.dns_records, name="portal_dns_records"),
    path('add-features', views.add_features, name="portal_add_features"),
    path('priority-support', views.priority_support, name="portal_priority_support"),

    path('', include('allauth.urls')),
]