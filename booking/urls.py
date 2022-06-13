from django.urls import path
from . import views

urlpatterns = [
    path('booking_day', views.booking_day, name='booking_day'),
    path('booking_detail', views.booking_detail, name='booking_detail'),
    path('booking_date', views.booking_date, name='booking_date'),
    path('booking_date_list', views.booking_date_list, name='booking_date_list'),
]