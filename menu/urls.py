from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_menu, name='menu_page'),
    path('menu_list', views.MenuListView.as_view(), name='menu_list'),
    path('item_create_form', views.MenuCreateView.as_view(), name='item_create_form'),
    path('item_detail/<int:pk>', views.MenuDetailView.as_view(), name='item_detail'),
    path('item_update_form/<int:pk>', views.MenuUpdateView.as_view(), name='item_update_form'),
    path('item_delete/<int:pk>', views.MenuDeleteView.as_view(), name='item_delete'),
]
