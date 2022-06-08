from django.urls import path
from . import views 

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipes'),
    path('create_recipe', views.RecipeCreateView.as_view(), name='create_recipe'),
    path('recipe_detail/<int:pk>', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe_update/<int:pk>', views.RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipe_delete/<int:pk>', views.RecipeDeleteView.as_view(), name='recipe_delete'),
        ]
