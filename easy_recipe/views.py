from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def recipes(request):
    return render(request, 'easy_recipe/recipes.html')