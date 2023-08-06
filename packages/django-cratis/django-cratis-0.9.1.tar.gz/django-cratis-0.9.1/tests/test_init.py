import os
from subprocess import check_output

from cratis.bootstrap import init_app, run_env_command
from tests._markers import slow


@slow
def test_init_in_empty_dir(tmpdir):
    """
    Test check simple operations like open file by path,
    load and save on existing file.

    :param tmpdir:
    :return:
    """

    with tmpdir.as_cwd():
        init_app(cratis_path=os.path.dirname(os.path.dirname(__file__)))

        assert tmpdir.join('settings.py').exists()
        assert tmpdir.join('.pyvenv').exists()

        out = check_output(['.pyvenv/bin/django-manage', 'check'])

        # make sure application is loading
        assert b'System check identified no issues' in out

@slow
def test_init_with_settings_and_repo_package(tmpdir):

    with tmpdir.as_cwd():
        with tmpdir.join('settings.py').open('w') as f:
            f.write(
"""
from cratis.settings import CratisConfig
from features import HelloFeature


class Dev(CratisConfig):
    # boo
    DEBUG = True
    SECRET_KEY = '123'
    """)

        init_app()

        # make sure file is not overriden
        assert '# boo' in  tmpdir.join('settings.py').read()



