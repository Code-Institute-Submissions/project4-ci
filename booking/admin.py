from django.contrib import admin
from .models import TimeSlot, Closed

@admin.register(TimeSlot)
class TimeslotAdmin(admin.ModelAdmin):

    list_filter = ('date',
                   'time',
                   'first_name',
                   'last_name',
                   'number_of_people',
                   'phone'
                   )
    list_display = ('date', 
                    'time',
                    'first_name',
                    'last_name',
                    'number_of_people',
                    'phone'
                    )
    search_fields = ['time', 'day', 'last_name']
    
@admin.register(Closed)
class ClosedAdmin(admin.ModelAdmin):

    list_filter = ('day', 'reason', 'user')
    list_display = ('user', 'day', 'reason')
    search_fields = ['time', 'day', 'reason']