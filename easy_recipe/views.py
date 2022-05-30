from django.shortcuts import render

# Create your views here.
def recipes(request):
    return render(request, 'easy_recipe/recipes.html')