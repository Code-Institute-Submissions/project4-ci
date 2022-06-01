from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import RecipePost

@login_required(redirect_field_name='account_login')
def recipes(request):
    recipes = RecipePost.objects.all()
    return render(request, 'easy_recipe/recipes.html', {'recipes': recipes})

