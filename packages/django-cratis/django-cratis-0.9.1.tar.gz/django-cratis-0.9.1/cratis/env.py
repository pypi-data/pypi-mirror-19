import os
import sys

import pip


def check_settings_module_or_exit(env=None):
    try:
        return __import__(os.environ['DJANGO_SETTINGS_MODULE'])
    except ImportError as m:
        print('Can not load settings module. Wrong directory?')
        print('-' * 50)
        print('Error: %s' % m)
        print()

        print()

        raise m


def load_env():
    os.environ['DJANGO_SETTINGS_MODULE'] = os.environ.get('DJANGO_SETTINGS_MODULE', 'settings')

    app_path = os.environ.get('CRATIS_APP_PATH', os.getcwd())
    sys.path = [app_path] + sys.path

    check_settings_module_or_exit()
