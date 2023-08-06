

def test_wsgi():
    from cratis.wsgi import application

def test_urls():
    from cratis.urls import urlpatterns

def test_django():
    from cratis.django import manage_command
    manage_command(['django', 'check'])