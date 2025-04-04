"""
WSGI config for mutts project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

import os
from django.core.wsgi import get_wsgi_application
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mutts.settings")

application = get_wsgi_application()

# 👇 Add this line for Vercel compatibility:
app = application
