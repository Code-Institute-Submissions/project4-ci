from django.shortcuts import render, reverse
from . import views
from .models import FoodMenu
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin

def food_menu(request):
    starters = FoodMenu.objects.filter(course=0)
    mains = FoodMenu.objects.filter(course=1)
    desserts = FoodMenu.objects.filter(course=2)
    return render(request, 'menu/menu_page.html', {'starters': starters, 'mains': mains, 'desserts': desserts})

class MenuListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = FoodMenu
    context_object_name = 'fooditems'
    template_name = 'menu/menu_list.html'
    
    def test_func(self):
        return self.request.user.is_staff

class MenuDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = FoodMenu
    context_object_name = 'fooditems'
    template_name = 'menu/item_detail.html'

    def test_func(self):
        return self.request.user.is_staff


class MenuCreateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = FoodMenu
    template_name = 'menu/item_create_form.html'
    success_message = 'New menu item created successfully'
    fields = [
        'title',
        'description',
        'course', 
        'price',
        ]

    def test_func(self):
        return self.request.user.is_staff
    
    def get_success_url(self):
        return reverse('item_detail', args=[self.object.pk])

class MenuUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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
    
    def test_func(self):
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse('item_detail', args=[self.object.pk])


class MenuDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FoodMenu
    template_name = 'menu/item_delete.html'
    success_message = 'Menu item deleted successfully'
    success_url = reverse_lazy('menu_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MenuDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff