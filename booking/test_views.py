from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from .models import Closed




class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user = User.objects.create_superuser('admin', 'admin@mail.com', 'adminpassword')


    def test_get_booking_day_page(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('booking_day'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/booking_day.html')

    def test_get_booking_day_unauthorize(self):
        response = self.client.get(reverse('booking_day'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/booking/booking_day')
    
    def test_get_booking_detail_page(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('booking_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/booking_detail.html')


    def test_get_customer_booking_list_page(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('customer_booking_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/customer_booking_list.html')

    def test_get_booking_date_list_page_unauthorized(self):
        response = self.client.get(reverse('booking_date_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/login/?next=/booking/booking_date_list')
    
    def test_get_booking_date_list_page_authorized(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('booking_date_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/booking_date_list.html')

    def test_get_closed_days_page_unauthorized(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('closed_list'))
        self.assertEqual(response.status_code, 403)

    def test_get_closed_days_page_authorised(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('closed_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/closed_list.html')
    
    def test_get_closed_detail_view(self):
        self.client.login(username='admin', password='adminpassword')
        day = Closed.objects.create(day='2022-12-25',
                                    reason='Christmas day',
                                    user=self.user
                                    )
        response = self.client.get(f'/booking/closed_detail/{day.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/closed_detail.html')


    def test_get_closed_create_page(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('closed_create_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/closed_create_form.html')

    def test_can_post_closed_create_form(self):
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
        
    def test_edit_closed(self):
        """Function to check whether a closed can be updated."""
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