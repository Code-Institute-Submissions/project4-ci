from django.shortcuts import render
from .models import TimeSlot

def booking_day(request):
    return render(request, 'booking/booking_day.html', {})

def booking_detail(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        bookings = TimeSlot.objects.filter(date=date)
        if len(bookings) > 0:
            pass
        else:
            times = ['12:00', '12:30', '13:00', '13:30', '14:00', '14:30',
                    '15:00', '15:30', '16:00', '16:30', '17:00', '17:30',
                    '18:00', '18:30', '19:00', '19:30', '20:00', '20:30']

    return render(request, 'booking/booking_detail.html', {'bookings': bookings, 'date': date, 'times': times})