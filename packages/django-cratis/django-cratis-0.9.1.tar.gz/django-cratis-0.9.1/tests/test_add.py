
import pytest
from cratis.add import parse_repo_parts, Url, compile_url, add_cmd
from cratis.bootstrap import init_app, run_env_command
from tests._markers import slow


@pytest.mark.parametrize("url,expected", [
    ("admin", Url(
        feature='cratis-admin',
        user='django-cratis',
        version='master',
        repo='cratis-admin',
        protocol='git+https'
    )),
    ("admin.", Url(
        feature='admin',
        user='django-cratis',
        version='master',
        repo='admin',
        protocol='git+https'
    )),
    ("admin@boo", Url(
        feature='cratis-admin',
        user='boo',
        version='master',
        repo='cratis-admin',
        protocol='git+https'
    )),
    ("admin@boo#dev", Url(
        feature='cratis-admin',
        user='boo',
        version='dev',
        repo='cratis-admin',
        protocol='git+https'
    )),
    ("ssh:baz.@foo/bar#dev", Url(
        feature='baz',
        user='foo',
        version='dev',
        repo='bar',
        protocol='git+ssh'
    )),
])
def test_repo_parts(url, expected):
    result = parse_repo_parts(url)

    assert result == expected


@pytest.mark.parametrize("params, url", [
    (Url(
        feature='baz',
        user='foo',
        version='dev',
        repo='bar',
        protocol='git+ssh'
    ), 'git+ssh://github.com/foo/bar.git@dev#egg=baz'),
])
def test_compile_url(params, url):
    result = compile_url(params)

    assert result == url

@slow
def test_install_admin(tmpdir):

    with tmpdir.as_cwd():
        init_app()

        add_cmd('admin')

        settings = tmpdir.join('settings.py').read()
        assert 'cratis_admin.features import AdminArea' in settings
        assert 'AdminArea(' in settings