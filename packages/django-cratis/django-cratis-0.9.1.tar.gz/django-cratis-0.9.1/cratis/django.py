import os
import sys

from cratis.env import load_env


def manage_command(args=None):

    if os.environ.get('DEBUG') == '1':
        import pydevd
        pydevd.settrace('localhost', port=33322, stdoutToServer=False, stderrToServer=False, suspend=False)

    load_env()

    from django.core.management import execute_from_command_line

    execute_from_command_line(args or sys.argv)
