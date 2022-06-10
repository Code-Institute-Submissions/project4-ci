from django.urls import path
from . import views

urlpatterns = [
    path('booking_day', views.booking_day, name='booking_day'),
    path('booking_detail', views.booking_detail, name='booking_detail'),
    # path('booking_create_form', views.BookingCreateView.as_view(), name='booking_create_form')
]