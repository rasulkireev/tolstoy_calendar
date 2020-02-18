# from celery.schedules import crontab
# from celery.task import periodic_task

# from .views import get_todays_quote_as_a_list
# from newsletter.models import Subscriber

# from django.template.loader import render_to_string


# @periodic_task(run_every=crontab(hour="8", minute="0"))
# def send_newsletter(self, request):
#     paragraphs = get_todays_quote_as_a_list()
#     subscribers = Subscriber.objects.filter(confirmed=True)

#     message_context = {
#         'delete_uri': request.build_absolute_uri('/delete/'),
#         'email': sub.email,
#         'conf_number': sub.conf_num,
#         'paragraphs': paragraphs
#         }

#     html_content = render_to_string('newsletter/emails/daily_html.html', message_context)

#     for sub in subscribers:
#         message = Mail(
#                 from_email=settings.FROM_EMAIL,
#                 to_emails=sub.email,
#                 subject=date_stringer_ru,
#                 html_content=contents)

#         sg.send(message)