from __future__ import absolute_import
import sys


# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
try:
    from .celery import app as celery_app
except ImportError:
    sys.stdout.write('Celery not found')


__VERSION__ = '0.1dev'