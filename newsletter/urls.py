from django.urls import path
from .views import new_subscriber, confirm, delete, send_newsletter

urlpatterns = [
    path('', new_subscriber, name='new_subscriber'),
    path('confirm/', confirm, name='confirm'),
    path('delete/', delete, name='delete'),

    path('sn', send_newsletter, name='send_newsletter'),
    ]

