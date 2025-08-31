import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.enable_utc = False

app.conf.beat_schedule = {
    'update-parsed-data-every-3-days': {
        'task': 'apps.multiparser.tasks.update_parsed_data_periodic',
        'schedule': crontab(hour=2, minute=0, day_of_week='*/3'),
    },
    'cleanup-old-files-weekly': {
        'task': 'apps.multiparser.tasks.cleanup_old_files',
        'schedule': crontab(hour=3, minute=0, day_of_week=0),
    },
}

