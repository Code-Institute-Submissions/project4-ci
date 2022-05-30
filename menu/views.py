from django.shortcuts import render
from . import views

def food_menu(request):
    return render(request, 'menu/menu_page.html', {})