from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from newsletter.models import Subscriber
from newsletter.forms import SubscriberForm

import random
import pandas as pd
import datetime as dt

def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

@csrf_exempt
def new_subscriber(request):
    if request.method == 'POST':
        sub = Subscriber(email=request.POST['email'], conf_num=random_digits())
        sub.save()
        message = Mail(
            from_email=settings.POSTMARK_SENDER,
            to_emails=sub.email,
            subject='Подтверждение Подписки',
            html_content='Спасибо за подписку! \
                Остался последний шаг. Перейдите по следующей ссылке чтобы завершить процесс. \
                <a href="{}/confirm/?email={}&conf_num={}"></a>.' \
                .format(request.build_absolute_uri('/confirm/'),
                                                    sub.email,
                                                    sub.conf_num))
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return render(request, 'index.html', {'email': sub.email, 'action': 'added', 'form': SubscriberForm()})
    else:
        return render(request, 'index.html', {'form': SubscriberForm()})


def confirm(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        return render(request, 'index.html', {'email': sub.email, 'action': 'confirmed'})
    else:
        return render(request, 'index.html', {'email': sub.email, 'action': 'denied'})


def delete(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.delete()
        return render(request, 'index.html', {'email': sub.email, 'action': 'unsubscribed'})
    else:
        return render(request, 'index.html', {'email': sub.email, 'action': 'denied'})


df = pd.read_csv('support/data/tolstoy-calendar.csv')

today = dt.datetime.today()
month = today.month
day = today.day
row = df[ (df['month']==month) & (df['day'] == day) ]
message = ' '.join(row['text'])


print(text)

def send_newsletter():
    send_mail(
    'Subject here',
    'Here is the message.',
    settings.POSTMARK_SENDER,
    Subscriber.objects.filter(confirmed=True),
    fail_silently=False,
    )
