from django.contrib import admin
from . models import RecipePost


@admin.register(RecipePost)
class RecipeAdmin(admin.ModelAdmin):
    """
    Registering the RecipePost database in the admin panel.
    Setting list display and filter items
    """

    list_filter = ('title', 'author', 'created_on')
    list_display = ('title', 'author', 'created_on')
    search_fields = ['title', 'author', 'created_on']
