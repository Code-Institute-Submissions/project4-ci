from django.shortcuts import render, reverse
from . import views
from .models import FoodMenu
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin

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


class MenuCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = FoodMenu
    template_name = 'menu/item_create_form.html'
    success_message = 'New menu item created successfully'
    fields = [
        'title',
        'description',
        'course', 
        'price',
        ]
    
    def get_success_url(self):
        return reverse('item_detail', args=[self.object.pk])

class MenuUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = FoodMenu
    context_object_name = 'fooditems'
    template_name = 'menu/item_update_form.html'
    success_message = 'Menu item updated successfully'
    fields = [
        'title',
        'description',
        'course', 
        'price',
        ]
    
    def get_success_url(self):
        return reverse('item_detail', args=[self.object.pk])


class MenuDeleteView(LoginRequiredMixin, DeleteView):
    model = FoodMenu
    template_name = 'menu/item_delete.html'
    success_message = 'Menu item deleted successfully'
    success_url = reverse_lazy('menu_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MenuDeleteView, self).delete(request, *args, **kwargs)