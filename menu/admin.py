from django.contrib import admin
from . models import FoodMenu


@admin.register(FoodMenu)
class MenuAdmin(admin.ModelAdmin):

    list_filter = ('title', 'course')
    list_display = ('title', 'course')
    search_fields = ['course']