from django.urls import path
from . import views

urlpatterns = [
    path('booking_day', views.booking_day, name='booking_day'),
    path('booking_detail', views.booking_detail, name='booking_detail'),
    path('booking_date', views.booking_date, name='booking_date'),
    path('booking_date_list', views.booking_date_list, name='booking_date_list'),
    path('closed_list', views.ClosedListView.as_view(), name='closed_list'),
    path('closed_detail/<int:pk>', views.ClosedDetailView.as_view(), name='closed_detail'),
    path('closed_delete/<int:pk>', views.ClosedDeleteView.as_view(), name='closed_delete'),
    path('closed_update_form/<int:pk>', views.ClosedUpdateView.as_view(), name='closed_update_form'),
    path('closed_create_form', views.ClosedCreateView.as_view(), name='closed_create_form'),
]