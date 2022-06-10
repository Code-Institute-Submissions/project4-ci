from django.contrib import admin
from .models import TimeSlot, Closed

@admin.register(TimeSlot)
class TimeslotAdmin(admin.ModelAdmin):

    list_filter = ('date', 'time', 'user', 'number_of_people')
    list_display = ('user', 'date', 'time', 'number_of_people')
    search_fields = ['time', 'day', 'user']
    
@admin.register(Closed)
class ClosedAdmin(admin.ModelAdmin):

    list_filter = ('day', 'reason', 'user')
    list_display = ('user', 'day', 'reason')
    search_fields = ['time', 'day', 'reason']