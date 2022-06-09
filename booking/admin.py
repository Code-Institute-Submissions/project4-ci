from django.contrib import admin
from .models import TimeSlot, Closed


@admin.register(TimeSlot)
class TimeslotAdmin(admin.ModelAdmin):

    list_filter = ('date', 'time')
    list_display = ('user', 'date', 'time')
    search_fields = ['time', 'date']
    
    
@admin.register(Closed)
class ClosedAdmin(admin.ModelAdmin):

    list_filter = ('day', 'reason', 'user')
    list_display = ('user', 'day', 'reason')
    search_fields = ['time', 'day', 'reason']