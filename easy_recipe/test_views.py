from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth.models import User




class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_get_recipe_list(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'easy_recipe/recipes.html')
    
    def test_get_recipe_create_page(self):
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'accounts/login.html')