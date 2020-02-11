from django.urls import path
from .views import new_subscriber, confirm, delete

urlpatterns = [
    path('', new_subscriber, name='new_subscriber'),
    path('confirm/', confirm, name='confirm'),
    path('delete/', delete, name='delete'),
    ]

