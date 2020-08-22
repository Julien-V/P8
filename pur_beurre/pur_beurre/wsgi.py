"""
WSGI config for pur_beurre project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get('IS_HEROKU', False):
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE', 'pur_beurre.pur_beurre.settings')
else:
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE', 'pur_beurre.settings')

application = get_wsgi_application()
