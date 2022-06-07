from django.shortcuts import render
from . import views
from .models import FoodMenu

def food_menu(request):
    starters = FoodMenu.objects.filter(course=0)
    mains = FoodMenu.objects.filter(course=1)
    desserts = FoodMenu.objects.filter(course=2)
    return render(request, 'menu/menu_page.html', {'starters': starters, 'mains': mains, 'desserts': desserts})