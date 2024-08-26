import os
from celery import Celery

# change myproject with your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
app = Celery("backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True)
def debg_task(self):
    print(f'Request: {self.request!r}')