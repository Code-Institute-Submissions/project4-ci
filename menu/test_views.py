from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.client import Client

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user = User.objects.create_superuser('admin', 'admin@mail.com', 'adminpassword')

    def test_get_menu_page(self):
        response = self.client.get(reverse('menu_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/menu_page.html')

    def test_get_menu_list_page_authorized(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('menu_list'))
        self.assertAlmostEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/menu_list.html')

    def test_get_menu_list_page_unauthorized(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('menu_list'))
        self.assertAlmostEqual(response.status_code, 403)

    # def test_get_menu_delete_item_page_unauthorizes_user(self):
    #     self.client.login(username='john', password='johnpassword')
    #     response = self.client.get(reverse('item_delete'))
    #     self.assertEqual(response.status_code, 403)
    
    def test_get_item_create_form_page_unauthorizes_user(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('item_create_form'))
        self.assertEqual(response.status_code, 403)