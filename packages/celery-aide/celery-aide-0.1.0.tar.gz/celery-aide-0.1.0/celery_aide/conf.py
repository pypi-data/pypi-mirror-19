import os

CELERY_AIDE_QUEUE = os.environ.get('CELERY_AIDE_QUEUE', 'celery_aide')