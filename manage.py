#!/usr/bin/env python
import os
import sys
import environ

env = environ.Env(
    PRODUCTION_ENV=(bool, False),
)
environ.Env.read_env(env.str('ENV_PATH', 'engine/settings/.env'))

if __name__ == "__main__":
    PRODUCTION_ENV = env('PRODUCTION_ENV')
    if PRODUCTION_ENV:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "engine.settings.production")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "engine.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
