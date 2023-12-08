import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")

app = Celery("django_app")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "scheduled-task-1": {
        "task": "apps.core.users.tasks.check_expiry",
        "schedule": crontab(hour="*", minute="0"),
        "args": (),
    },
}

# WARNING: Changing the timezone in django can affect the periodic tasks.
# This may require to reset the scheduler manually.
# app.conf.timezone = 'UTC'

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
