from celery.task.schedules import crontab
from celery.decorators import periodic_task

from newsletter.views import send_newsletter

@periodic_task(
    run_every=(crontab(minute=0, hour=8)), 
    name="send_newsletter", 
    ignore_result=True
)
def run():
    send_newsletter()
    
    