import psutil

from django.utils.safestring import mark_safe
from django.conf import settings

from engine import VERSION, AUTHOR, COMPANY, LICENSE, COPYRIGHT, CLIENT

from datetime import datetime
import pkg_resources

def get_cpu():
    """Gets the system-wide CPU utilisation percentage"""
    utilisation = list(psutil.cpu_percent(interval=1, percpu=True))
    cpu_data_utilisation = []
    load_avg_list = []
    cpu_data = {}
    for count in range(len(utilisation)):
        count = count + 1
        cpu_data_utilisation.append({
            "label" : str("CPU " + str(count)),
            "util" : round(utilisation[count-1])
        })
    load_avg_tuple = tuple(psutil.getloadavg())
    load_avg_1 = (load_avg_tuple[0]/len(cpu_data_utilisation)) * 100
    load_avg_5 = (load_avg_tuple[1]/len(cpu_data_utilisation)) * 100
    load_avg_15 = (load_avg_tuple[2]/len(cpu_data_utilisation)) * 100
    load_avg = {
        "1"  : round(load_avg_1),
        "5"  : round(load_avg_5),
        "15" : round(load_avg_15)
    }
    cpu_data = {
        "core_util" : cpu_data_utilisation,
        "load_avg"  : load_avg,
        'check_timestamp' : datetime.now(),
    }
    return cpu_data

def get_ram():
    """Returns free and used memory size"""
    mem = list(psutil.virtual_memory())
    total = mem[0]
    avail = mem[1]
    used = total - avail
    util_percent = (used/total) * 100
    free_percent = (avail/total) * 100
    memory_data = {
        'total' : total,
        'avail' : avail,
        'used'  : used,
        'util_percent' : util_percent,
        'free_percent' : free_percent,
        'check_timestamp' : datetime.now(),
    }
    return memory_data

def get_disk():
    """Returns free and used disk size"""
    disk = list(psutil.disk_usage(settings.DISK_MOUNT_POINT))
    total = disk[0]
    """
    # This is one way of doing it (probably the most efficient)
    # But the issue is, the used space reading from psutil is
    # inaccurate (around 5% off from the actual value) - this could
    # be simply due to my development environment, but I will not
    # be using psutil's used space reading, instead, I will calculate
    # used = total - free

    avail = disk[2]
    used = disk[1]
    """
    avail = disk[2]
    used = total - avail
    util_percent = (used/total) * 100
    free_percent = (avail/total) * 100
    disk_data = {
        'total' : total,
        'avail' : avail,
        'used'  : used,
        'util_percent' : util_percent,
        'free_percent' : free_percent,
        'check_timestamp' : datetime.now(),
    }

    return disk_data


def get_engine_version():
    """
    Simple template tag function that returns Engine's version when called.
    """
    return VERSION

def get_pip_requirements():
    """
    Returns all packages and version stated in requirements.txt.
    """
    requirements_packages_list = []
    requirements_packages = list(pkg_resources.working_set)
    for package in requirements_packages:
        requirements_packages_list.append(str(package.key) + " == " + str(package.version))
    return requirements_packages_list


def get_pip_list():
    """
    Returns list of Pip packages and their versions
    """
    installed_packages_list = []
    installed_packages = list(pkg_resources.working_set)
    for package in installed_packages:
        installed_packages_list.append(str(package.project_name) + " @ " + str(package.parsed_version))
    return installed_packages_list


def diagnostics_report():
    """
    Returns dictionary of get_engine_version, get_pip_requirements and get_pip_list
    """
    report = {
        "engine_version": get_engine_version(),
        "requirements_txt": get_pip_requirements(),
        "pip_list": get_pip_list(),
    }
    return report

def get_sentry_release():
    """Gets the Sentry release name from settings.py"""
    return settings.SENTRY_RELEASE

def get_sentry_dsn():
    """Gets the Sentry DSN from settings.py"""
    return settings.SENTRY_DSN

def get_engine_author():
    """Gets the AUTHOR attribute from __init__.py"""
    return AUTHOR

def get_engine_company():
    """Gets the author's COMPANY attribute from __init__.py"""
    # COMPANY attribute will always return Web Mastered Ltd
    return COMPANY

def get_engine_license():
    """Gets the LICENSE attribute from __init__.py"""
    return LICENSE

def get_engine_copyright():
    """Gets the COPYRIGHT attribute from __init__.py"""
    return COPYRIGHT

def get_engine_client():
    """Gets the CLIENT attribute from __init__.py"""
    return CLIENT
