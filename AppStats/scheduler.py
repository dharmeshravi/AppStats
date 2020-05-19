from . import views
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler

def execute():
    scheduler = BackgroundScheduler()
    scheduler.add_job(views.scheduled_Job, 'interval', minutes=settings.DATA_LOAD_MINUTE_INTERVAL)
    scheduler.start()