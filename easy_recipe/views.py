from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import RecipePost
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

@login_required(redirect_field_name='account_login')
def recipes(request):
    recipes = RecipePost.objects.all()
    return render(request, 'easy_recipe/recipes.html', {'recipes': recipes})

class RecipeCreateView(CreateView):
    model = RecipePost 
    template_name = 'easy_recipe/recipe_create_form.html'
    fields = [
        'title',
        'author',
        'content', 
        'featured_image',
        'excerpt',
        ]

