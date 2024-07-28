import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "birthday.settings")

app = Celery("birthday")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=False)
def debug_task(self):
    print(f"Request: {self.request!r}")
    return "Task completed"
