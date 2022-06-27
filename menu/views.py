from django.shortcuts import render, reverse
from .models import FoodMenu
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin

def food_menu(request):
    """
    Function renders menu page
    """
    page_title = "Menu"
    starters = FoodMenu.objects.filter(course=0)
    mains = FoodMenu.objects.filter(course=1)
    desserts = FoodMenu.objects.filter(course=2)
    return render(request, 'menu/menu_page.html', {'starters': starters,
                                                   'mains': mains,
                                                   'desserts': desserts,
                                                   'page_title': page_title})

class MenuListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Displays list of menu items
    Extra context function: Gives extra context to 
    be used by template
    Test func: Tests if user is_staff
    """
    model = FoodMenu
    context_object_name = 'fooditems'
    template_name = 'menu/menu_list.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Menu'
        return context

class MenuDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Displays detail of menu item
    Extra context function: Gives extra context to 
    be used by template
    Test func: Tests if user is_staff
    """
    model = FoodMenu
    context_object_name = 'fooditems'
    template_name = 'menu/item_detail.html'

    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Menu'
        return context


class MenuCreateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Displays form to create new menu item
    Extra context function: Gives extra context to 
    be used by template
    Test func: Tests if user is_staff
    Get success func: Gets id of object created and returns 
    detail view url of item
    """
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Menu'
        return context

class MenuUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Displays form to update/edit menu item
    Extra context function: Gives extra context to 
    be used by template
    Test func: Tests if user is_staff
    Get success func: Gets id of object created and returns 
    detail view url of item
    """
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Menu'
        return context


class MenuDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Deletes menu item in database
    Extra context function: Gives extra context to 
    be used by template
    Test func: Tests if user is_staff
    Get success func: Gets id of object created and returns 
    detail view url of item
    def delete: displays message item was deleted
    """
    model = FoodMenu
    template_name = 'menu/item_delete.html'
    success_message = 'Menu item deleted successfully'
    success_url = reverse_lazy('menu_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MenuDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Menu'
        return context