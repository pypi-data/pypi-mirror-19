from cratis.env import load_env
from django.core.wsgi import get_wsgi_application

load_env()
application = get_wsgi_application()
