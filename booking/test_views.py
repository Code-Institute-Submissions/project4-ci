from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from .models import Closed, TimeSlot
from django.contrib import messages




class TestViews(TestCase):
    """
    Testing all the views for Booking. If you can access views authorized and 
    not authorized. Testing the edit/detail/create and delete methods
    """
    def setUp(self):
        """
        Setup  a user
        """
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user = User.objects.create_superuser('admin', 'admin@mail.com', 'adminpassword')

    def test_get_booking_day_page(self):
        """
        Function to test if booking_day page displays
        """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('booking_day'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/booking_day.html')

    def test_get_booking_day_unauthorize(self):
        """
        Function to test if you can access the booking_day 
        page without logging in
        """
        response = self.client.get(reverse('booking_day'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/booking/booking_day')
    
    def test_get_booking_detail_page(self):
        """
        Function to test if you can get the booking_detail page
        """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('booking_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/booking_detail.html')
    
    def test_get_booking_detail_page_unauthorized(self):
        """
        Function to test if you can get the booking_detail page
        if you are not logged in
        """
        response = self.client.get(reverse('booking_detail'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/booking/booking_detail')

    def test_can_post_booking_detail(self):
        """
        Function to test if you can make a booking and post data to 
        the database
        """
        self.client.login(username='john', password='johnpassword')
        booking = TimeSlot.objects.all()
        self.assertEqual(len(booking), 0)
        response = self.client.post('/booking/booking_detail',
                                    {'date': '2022-06-30',
                                     'first_name': 'John',
                                     'last_name': 'Doe',
                                     'time': '15:00',
                                     'user': self.user.id,
                                     'phone': '02323654456',
                                     'number_of_people': '4'})
        self.assertEqual(response.status_code, 302)
        new_bookings = TimeSlot.objects.all()
        self.assertEqual(len(new_bookings), 1)

    def test_get_booking_date_page(self):
        """
        Function to test if you can get the booking_date page
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('booking_date'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/booking_date.html')


    def test_get_booking_date_list_page_unauthorized(self):
        """
        Function to test if you can get the booking_date page if 
        you are not authorized
        """
        response = self.client.get(reverse('booking_date_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/login/?next=/booking/booking_date_list')
    
    def test_get_booking_date_list_page_authorized(self):
        """
        Function to test if you can get the booking_date_list page
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('booking_date_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/booking_date_list.html')


    def test_get_closed_days_page_unauthorized(self):
        """
        Function to test if you can get the closed_days page if 
        you are not authorized
        """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('closed_list'))
        self.assertEqual(response.status_code, 403)

    def test_get_closed_days_page_authorised(self):
        """
        Function to test if you can get the closed_days page if 
        you are authorized
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('closed_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/closed_list.html')

    def test_get_closed_details_page_unauthorized(self):
        """
        Function to test if you can get the closed_details page if 
        you are not authorized
        """
        self.client.login(username='john', password='johnpassword')
        day = Closed.objects.create(day='2022-12-25',
                                    reason='Christmas day',
                                    user=self.user
                                    )
        response = self.client.get(f'/booking/closed_detail/{day.id}')
        self.assertEqual(response.status_code, 403)
    
    def test_get_closed_detail_view(self):
        """
        Function to test if you can get the closed_details page if 
        you are authorized
        """
        self.client.login(username='admin', password='adminpassword')
        day = Closed.objects.create(day='2022-12-25',
                                    reason='Christmas day',
                                    user=self.user
                                    )
        response = self.client.get(f'/booking/closed_detail/{day.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/closed_detail.html')


    def test_get_closed_create_page(self):
        """
        Function to test if you can get the closed_create page if 
        you are authorized
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('closed_create_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/closed_create_form.html')

    def test_can_post_closed_create_form(self):
        """
        Function to test if you can create a new closed day
        """
        self.client.login(username='admin', password='adminpassword')
        items = Closed.objects.all()
        self.assertEqual(len(items), 0)
        response = self.client.post('/booking/closed_create_form',
                                    {'day': '2022-12-25',
                                    'reason': 'Christmas day',
                                    'user': self.user.id})
        self.assertEqual(response.status_code, 302)
        new_items = Closed.objects.all()
        self.assertEqual(len(new_items), 1)

    def test_get_closed_delete_page(self):
        """ 
        Function to test is you can get the Closed_delete page
        """
        self.client.login(username='admin', password='adminpassword')
        item = Closed.objects.create(day='2022-12-25',
                                    reason='Christmas day',
                                    user=self.user
                                    )
        response = self.client.get(f'/booking/closed_delete/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/closed_delete.html')

    def test_delete_closed(self):
        """Function to check whether a closed day can be deleted."""
        self.client.login(username='admin', password='adminpassword')
        item = Closed.objects.create(day='2022-12-25',
                                    reason='Christmas day',
                                    user=self.user
                                    )
        existing_items = Closed.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 1)
        response = self.client.post(f'/booking/closed_delete/{item.id}')
        self.assertEqual(response.status_code, 302)
        existing_items = Closed.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 0)

    def test_get_closed_update_page(self):
        """
        Function to test if you can get the closed_update page
        """
        self.client.login(username='admin', password='adminpassword')
        item = Closed.objects.create(day='2022-12-25',
                                    reason='Christmas day',
                                    user=self.user
                                    )
        response = self.client.get(f'/booking/closed_update_form/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/closed_update_form.html') 

    def test_edit_closed(self):
        """Function to check whether a closed day can be updated."""
        self.client.login(username='admin', password='adminpassword')
        item = Closed.objects.create(day='2022-12-25',
                                    reason='Christmas day',
                                    user=self.user
                                    )
        response = self.client.post(f'/booking/closed_update_form/{item.id}',
                                    {
                                        'day': '2022-12-25',
                                        'reason': 'Christmas day Test',
                                        'user': self.user.id,
                                    })
        self.assertEqual(response.status_code, 302)
        updated_item = Closed.objects.get(id=item.id)
        self.assertEqual(updated_item.reason, 'Christmas day Test')

    def test_get_customer_booking_list_view(self):
        """
        Function to test if you can get the customer_booking_list_view
        """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('customer_booking_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/customer_booking_list.html')

    def test_get_customer_booking_detail_page(self):
        """
        Function to test if you can get customer_booking_detail page
        """
        self.client.login(username='john', password='johnpassword')
        booking = TimeSlot.objects.create(date='2022-06-30',
                                          first_name='John',
                                          last_name='Doe',
                                          time='15:00',
                                          user=self.user,
                                          phone='02323654456',
                                          number_of_people='4')
        response = self.client.get(f'/booking/customer_booking_detail/{booking.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/customer_booking_detail.html')

    def test_get_customer_booking_delete_page(self):
        """
        Function to test if you can get the customer_booking_delete page
        """
        self.client.login(username='john', password='johnpassword')
        booking = TimeSlot.objects.create(date='2022-06-30',
                                          first_name='John',
                                          last_name='Doe',
                                          time='15:00',
                                          user=self.user,
                                          phone='02323654456',
                                          number_of_people='4')
        response = self.client.get(f'/booking/booking_delete/{booking.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/customer_booking_delete.html')  
    
    def test_customer_booking_delete_page(self):
        """
        Function to test if you can delete a booking
        """
        self.client.login(username='john', password='johnpassword')
        booking = TimeSlot.objects.create(date='2022-06-30',
                                          first_name='John',
                                          last_name='Doe',
                                          time='15:00',
                                          user=self.user,
                                          phone='02323654456',
                                          number_of_people='4')
        booking_list = TimeSlot.objects.all()
        self.assertEqual(len(booking_list), 1)
        response = self.client.post(f'/booking/booking_delete/{booking.id}')
        self.assertEqual(response.status_code, 302)
        new_booking_list = TimeSlot.objects.all()
        self.assertEqual(len(new_booking_list), 0)

    def test_booking_detail_post_on_fully_booked_time(self):
        """
        Function to test if you can over book a timeslot
        """
        self.client.login(username='john', password='johnpassword')
        booking1 = TimeSlot.objects.create(date='2022-06-30',
                                          first_name='John',
                                          last_name='Doe',
                                          time='15:00',
                                          user=self.user,
                                          phone='02323654456',
                                          number_of_people='4')
        booking2 = TimeSlot.objects.create(date='2022-06-30',
                                          first_name='John',
                                          last_name='Doe',
                                          time='15:00',
                                          user=self.user,
                                          phone='02323654456',
                                          number_of_people='4')
        booking3 = TimeSlot.objects.create(date='2022-06-30',
                                          first_name='John',
                                          last_name='Doe',
                                          time='15:00',
                                          user=self.user,
                                          phone='02323654456',
                                          number_of_people='4')
        booking4 = TimeSlot.objects.create(date='2022-06-30',
                                          first_name='John',
                                          last_name='Doe',
                                          time='15:00',
                                          user=self.user,
                                          phone='02323654456',
                                          number_of_people='4')
        booking5 = TimeSlot.objects.create(date='2022-06-30',
                                          first_name='Peter',
                                          last_name='Doe',
                                          time='15:00',
                                          user=self.user,
                                          phone='02323654456',
                                          number_of_people='4')
        bookings = TimeSlot.objects.filter(time='15:00',date='2022-06-30')
        self.assertEqual(len(bookings), 5)
        response = self.client.post('/booking/booking_detail',
                                    {'date': '2022-06-30',
                                     'first_name': 'John',
                                     'last_name': 'Doe',
                                     'time': '15:00',
                                     'user': self.user.id,
                                     'phone': '02323654456',
                                     'number_of_people': '4'})
        self.assertEqual(response.status_code, 200)
        self.assertRaisesMessage(messages.success, 'Sorry please choose another time')

    def test_get_closed_days_booking_detail(self):
        """
        Function to test if you can get the closed day detail
        """
        item = Closed.objects.create(day='2022-12-25',
                                    reason='Christmas day',
                                    user=self.user
                                    )
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('booking_detail'))
        self.assertEqual(len(response.context['closed_days']), 1)
       
