from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import TimeSlot, Closed





@login_required
def booking_day(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    bookings = TimeSlot.objects.filter(user=user)
    return render(request, 'booking/booking_day.html', {'bookings': bookings})

@login_required
def booking_detail(request):
    date = request.GET.get('date')
    bookings = TimeSlot.objects.filter(date=date)
    days = Closed.objects.all()
    closed_days = []
    days = Closed.objects.all()
    for day in days:
        closed_days.append(day.day.strftime("%Y-%m-%d"))
    
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

    if request.method == 'POST':
        current_user = request.user
        date = request.POST.get('date')
        time = request.POST.get('time')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        user = User.objects.get(id=current_user.id)
        number_of_people = request.POST.get('number_of_people')
        form = TimeSlot(date=date,
                        first_name=first_name,
                        last_name=last_name,
                        time=time,
                        user=user,
                        phone=phone,
                        number_of_people=number_of_people
                        )
        form.save()
        return redirect('booking_day')
    return render(request, 'booking/booking_detail.html', 
                  {'bookings': bookings,
                   'date': date,
                   'times': times,
                   'closed_days': closed_days
                   })
@login_required
def booking_date(request):
    return render(request, 'booking/booking_date.html')

@login_required
def booking_date_list(request):
    date = request.GET.get('date')
    bookings = TimeSlot.objects.filter(date=date)

    return render(request, 'booking/booking_date_list.html', {'bookings': bookings,'date': date})

    
class ClosedListView(LoginRequiredMixin, ListView):
    model = Closed
    context_object_name = 'dates'
    template_name = 'booking/closed_list.html'

class ClosedDetailView(LoginRequiredMixin, DetailView):
    model = Closed
    context_object_name = 'dates'
    template_name = 'booking/closed_detail.html'


class ClosedCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Closed 
    template_name = 'booking/closed_create_form.html'
    success_url = reverse_lazy('closed_list')
    success_message = 'Date added successfully'
    fields = [
        'day',
        'reason',
        'user', 
        ]

class ClosedUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Closed
    context_object_name = 'dates'
    template_name = 'booking/closed_update_form.html'
    success_message = 'Date updated successfully'
    success_url = reverse_lazy('closed_list')
    fields = [
        'day',
        'reason',
        'user',
        ]


class ClosedDeleteView(LoginRequiredMixin, DeleteView):
    model = Closed
    template_name = 'booking/closed_delete.html'
    success_message = 'Date deleted successfully!'
    success_url = reverse_lazy('closed_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ClosedDeleteView, self).delete(request, *args, **kwargs)

class CustomerBookingListView(LoginRequiredMixin, ListView):
    model = TimeSlot
    context_object_name = 'timeslots'
    template_name = 'booking/customer_booking_list.html'

class CustomerBookingDetailView(LoginRequiredMixin, DetailView):
    model = TimeSlot
    context_object_name = 'timeslots'
    template_name = 'booking/customer_booking_detail.html'

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = TimeSlot
    template_name = 'booking/customer_booking_delete.html'
    success_message = 'Date deleted successfully!'
    success_url = reverse_lazy('booking_day')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(BookingDeleteView, self).delete(request, *args, **kwargs)