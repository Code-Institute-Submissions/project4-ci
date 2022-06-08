from django.shortcuts import render
from .models import TimeSlot

def booking_day(request):
    times = TimeSlot.objects.filter(time='13:00')
    return render(request, 'booking/booking_day.html', {'times': times})
    