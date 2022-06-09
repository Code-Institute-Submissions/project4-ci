from django.contrib import admin
from .models import TimeSlot


@admin.register(TimeSlot)
class TimeslotAdmin(admin.ModelAdmin):

    list_filter = ('date', 'time')
    list_display = ('user', 'date', 'time')
    search_fields = ['time', 'date']
    
