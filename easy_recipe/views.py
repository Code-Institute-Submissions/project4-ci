from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from .models import RecipePost
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class RecipeListView(LoginRequiredMixin, ListView):
    model = RecipePost
    context_object_name = 'recipes'
    template_name = 'easy_recipe/recipes.html'


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = RecipePost
    context_object_name = 'recipe'
    template_name = 'easy_recipe/recipe_detail.html'


class RecipeCreateView( LoginRequiredMixin, CreateView):
    model = RecipePost 
    template_name = 'easy_recipe/recipe_create_form.html'
    success_url = reverse_lazy('recipes')
    fields = [
        'title',
        'author',
        'content', 
        'featured_image',
        'excerpt',
        ]

class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = RecipePost 
    context_object_name = 'recipe'
    template_name = 'easy_recipe/recipe_update_form.html'
    success_url = reverse_lazy('recipes')
    fields = [
        'title',
        'author',
        'content', 
        'featured_image',
        'excerpt',
        ]


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = RecipePost
    template_name = 'easy_recipe/recipe_delete.html'
    success_url = reverse_lazy('recipes')
    