from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from dashboard.metrics import get_cpu, get_ram, get_disk, diagnostics_report

def metrics(request):
    metrics_response_data = {
        "cpu"    : get_cpu(),
        "ram"    : get_ram(),
        "disk"   : get_disk(),
        "report" : diagnostics_report(),
    }
    return JsonResponse(metrics_response_data)