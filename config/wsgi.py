"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Run migrations automatically at startup
try:
  call_command('migrate', interactive=False)
except Exception as e:
  # Optional: print error, but don’t crash the app
  print(f"Migration error: {e}")

application = get_wsgi_application()
