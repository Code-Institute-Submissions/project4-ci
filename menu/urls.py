from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_menu, name='menu_page'),
]
