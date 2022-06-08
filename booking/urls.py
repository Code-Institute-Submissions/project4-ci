from django.urls import path
from . import views

urlpatterns = [
    path('booking_day', views.booking_day, name='booking_day')
]