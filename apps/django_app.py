import os
import sys

from django.conf import settings
from django.core import management
from django.core.wsgi import get_wsgi_application
from django.shortcuts import redirect

try:
    from django.urls import re_path as compat_url
except ImportError:
    from django.conf.urls import url as compat_url

from vulnpy.django import vulnerable_urlpatterns


urlpatterns = [
    compat_url(r"^$", lambda r: redirect("/vulnpy"))
] + vulnerable_urlpatterns

if not settings.configured:
    settings.configure(
        **{
            "ROOT_URLCONF": "django_app"
            if __name__ == "__main__"
            else "apps.django_app",
            "SECRET_KEY": os.environ.get("DJANGO_SECRET_KEY", os.urandom(32).hex()),
            "DEBUG": os.environ.get("DJANGO_DEBUG", "false").lower() == "true",
            "ALLOWED_HOSTS": os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]").split(","),
            "WSGI_APPLICATION": "django_app.vulnpy_app",
        }
    )

vulnpy_app = get_wsgi_application()

if os.environ.get("VULNPY_USE_CONTRAST"):
    from contrast.django import ContrastMiddleware

    vulnpy_app = ContrastMiddleware(vulnpy_app)

if __name__ == "__main__":
    management.execute_from_command_line(sys.argv)
