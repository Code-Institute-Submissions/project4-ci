from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth.models import User




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
    
    # def test_get_booking_detail_page(self):
    #     self.client.login(username='john', password='johnpassword')
    #     response = self.client.get(reverse('booking_detail'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'booking/booking_detail.html')


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

    def test_get_closed_days_unauthorized(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('closed_list'))
        self.assertEqual(response.status_code, 403)

    def test_get_closed_days_page_authorised(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('closed_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/closed_list.html')