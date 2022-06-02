from django.urls import path
from . import views
from .views import RecipeCreateView

urlpatterns = [
    path('', views.recipes, name='recipes'),
    path('create_recipe', views.RecipeCreateView.as_view(), name='create_recipe')
        ]
