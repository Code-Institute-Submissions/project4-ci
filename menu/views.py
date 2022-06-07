from django.shortcuts import render
from . import views
from .models import FoodMenu
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

def food_menu(request):
    starters = FoodMenu.objects.filter(course=0)
    mains = FoodMenu.objects.filter(course=1)
    desserts = FoodMenu.objects.filter(course=2)
    return render(request, 'menu/menu_page.html', {'starters': starters, 'mains': mains, 'desserts': desserts})

class MenuListView(LoginRequiredMixin, ListView):
    model = FoodMenu
    context_object_name = 'fooditems'
    template_name = 'menu/menu_list.html'

class MenuDetailView(LoginRequiredMixin, DetailView):
    model = FoodMenu
    context_object_name = 'fooditems'
    template_name = 'menu/item_detail.html'


class MenuCreateView( LoginRequiredMixin, CreateView):
    model = FoodMenu
    template_name = 'menu/item_create_form.html'
    success_url = reverse_lazy('menu_list')
    fields = [
        'title',
        'description',
        'course', 
        'price',
        ]

class MenuUpdateView(LoginRequiredMixin, UpdateView):
    model = FoodMenu
    context_object_name = 'fooditems'
    template_name = 'menu/item_update_form.html'
    success_url = reverse_lazy('menu_list')
    fields = [
        'title',
        'description',
        'course', 
        'price',
        ]


class MenuDeleteView(LoginRequiredMixin, DeleteView):
    model = FoodMenu
    template_name = 'menu/item_delete.html'
    success_url = reverse_lazy('menu_list')
    