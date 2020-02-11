from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

from newsletter.models import Subscriber
from newsletter.forms import SubscriberForm
from support.data.months import months_dict

import random
import pandas as pd
import datetime as dt

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail

def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

def date_stringer_ru():
    today = dt.datetime.today()
    month = today.month
    month_name = month_dict['month']
    day = today.day
    
    string_date = str(month_name) + ' ' + str(day)

    return string_date

@csrf_exempt
def new_subscriber(request):
    if request.method == 'POST':
        sub = Subscriber(email=request.POST['email'], conf_num=random_digits())
        sub.save()

        message_context = {
            'absolute_uri':request.build_absolute_uri('/confirm/'),
            'sub_email':sub.email,
            'sub_conf':sub.conf_num
        }

        html_confirmation = render_to_string('newsletter/emails/confirm_subscription.html', message_context)
        
        message = Mail(
            from_email = settings.FROM_EMAIL,
            to_emails = sub.email,
            subject = 'Подтверждение Подписки',
            html_content = html_confirmation)
            
            
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except:
            print(e.message)

        return render(request, 'newsletter/template_index.html', {'email': sub.email, 'action': 'added', 'form': SubscriberForm()})
    else:
        return render(request, 'newsletter/template_index.html', {'form': SubscriberForm()})


def confirm(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        return render(request, 'newsletter/template_index.html', {'email': sub.email, 'action': 'confirmed'})
    else:
        return render(request, 'newsletter/template_index.html', {'email': sub.email, 'action': 'denied'})


def delete(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.delete()
        return render(request, 'newsletter/template_index.html', {'email': sub.email, 'action': 'unsubscribed'})
    else:
        return render(request, 'newsletter/template_index.html', {'email': sub.email, 'action': 'denied'})


def get_todays_quote_as_a_list():
    df = pd.read_csv('support/data/tolstoy-calendar-no-author.csv')

    today = dt.datetime.today()
    month = today.month
    day = today.day

    row = df[ (df['month']==month) & (df['day'] == day) ]
    message = row['text'].to_list()

    return message


def send_newsletter(self, request):
    paragraphs = get_todays_quote_as_a_list()
    subscribers = Subscriber.objects.filter(confirmed=True)

    message_context = {
            'absolute_uri':request.build_absolute_uri('/confirm/'),
            'sub_email':sub.email,
            'sub_conf':sub.conf_num,
            'paragraphs':paragraphs
        }

    html_content = render_to_string('newsletter/emails/daily_html.html', message_context)

    for sub in subscribers:
        message = Mail(
                from_email=settings.FROM_EMAIL,
                to_emails=sub.email,
                subject=date_stringer_ru,
                html_content=contents + (
                    '<br><a href="{}/delete/?email={}&conf_num={}">Unsubscribe</a>.').format(
                        request.build_absolute_uri('/delete/'),
                        sub.email,
                        sub.conf_num))
        sg.send(message)
    