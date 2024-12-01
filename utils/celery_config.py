"""
This module configures the Celery application to run background tasks. It sets up the Celery instance
with the appropriate broker, backend, and task schedule. Additionally, it configures the timezone for the tasks.

Dependencies:
- celery.schedules.crontab: For scheduling periodic tasks using cron expressions.
- celery.Celery: The Celery framework for handling asynchronous tasks.
- utils.config_secrets.Config: Configuration file for accessing Redis URLs and other secrets.
"""

from celery.schedules import crontab
from celery import Celery
from utils.config_secrets import Config


app = Celery(
    "background-tasks",
    broker=Config.URL_REDIS,
    backend=Config.URL_REDIS,
    include=[
        "tasks.celery_tasks"
    ]
)

app.conf.beat_schedule = {
    "engine": {
        "task": "tasks.celery_tasks.check_student_status",
        "schedule": crontab(minute="*", hour="*")
    }
}

app.conf.timezone = "America/Mexico_City"
