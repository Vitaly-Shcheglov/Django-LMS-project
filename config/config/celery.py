import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('Django_LMS_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'notify-users-about-upcoming-courses-every-hour': {
        'task': 'courses.tasks.notify_users_about_upcoming_courses',
        'schedule': 3600.0,
    },
}

@app.task(bind=True)
def debug_task(self):
    """Пример задачи для отладки."""
    print(f'Request: {self.request!r}')
