from django.shortcuts import render
from .models import TimeSlot, Closed
from datetime import datetime

def booking_day(request):
    return render(request, 'booking/booking_day.html', {})

def booking_detail(request):
    
    if request.method == 'POST':

        # date entered by user in booking_day page
        date = request.POST.get('date')
        # queries database using date
        bookings = TimeSlot.objects.filter(date=date)
        # queries databse for daysed closed and extracts days and 
        # inserts into list
        days = Closed.objects.all()
        closed_days = []
        for day in days:
            closed_days.append(day.day.strftime("%Y-%m-%d"))
        # function looks for available times for date
        if len(bookings) > 0:
            times = ['12:00', '13:00','14:00',
                    '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00']
            # get times that is booked for date add them to list
            booked_times = []
            for booking in bookings:
                booked_times.append(booking.time)
            # count how many times ,time is in list and add to new list
            count_times = []
            for time in booked_times:
                count_times.append(booked_times.count(time))
            # see if item greater then predetermined amount
            # and add to list
            time = []
            counter = 0
            for num in count_times:
                counter += 1
                if num >= 5:
                    index_of = (counter-1)
                    time.append(str(booked_times[index_of]))
            time = list(dict.fromkeys(time))
            
            # removes times that is not available
            for slot in time:
                if slot in times:
                    times.remove(slot)
        else:
            times = ['12:00', '13:00', '14:00',
                     '15:00', '16:00', '17:00',
                     '18:00', '19:00', '20:00']

    return render(request, 'booking/booking_detail.html', 
                  {'bookings': bookings,
                   'date': date,
                   'times': times,
                   'closed_days': closed_days
                   })