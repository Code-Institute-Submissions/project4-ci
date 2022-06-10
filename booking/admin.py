from django.contrib import admin
from .models import TimeSlot, Closed

admin.site.register(TimeSlot)
    
@admin.register(Closed)
class ClosedAdmin(admin.ModelAdmin):

    list_filter = ('day', 'reason', 'user')
    list_display = ('user', 'day', 'reason')
    search_fields = ['time', 'day', 'reason']