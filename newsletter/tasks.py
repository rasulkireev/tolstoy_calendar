from celery.task.schedules import crontab
from celery.decorators import periodic_task

from newsletter.views import send_newsletter

@periodic_task(
    run_every=(crontab()), 
    name="send_newsletter", 
    ignore_result=True
)
def run():
    send_newsletter()
    
    