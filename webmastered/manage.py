#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # os.environ['DJANGO_SETTINGS_MODULE'] = str('engine.settings.') + str(os.environ.get('WSGI_SETTINGS_MODULE'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "engine.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
