from django.shortcuts import render
from .models import TimeSlot

def booking_day(request):
    return render(request, 'booking/booking_day.html', {})

def booking_detail(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        bookings = TimeSlot.objects.filter(date=date)

    return render(request, 'booking/booking_detail.html', {'bookings': bookings})