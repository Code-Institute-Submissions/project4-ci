from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from .models import RecipePost




class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user = User.objects.create_superuser('admin', 'admin@mail.com', 'adminpassword')


    def test_get_recipe_list_page_authorized_user(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'easy_recipe/recipes.html')
    
    def test_get_recipe_list_page_not_loggedin(self):
        response = self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/recipes/')
    
    def test_get_recipe_create_page_unauthorizes_user(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 403)

    def test_get_recipe_edit_page_unauthorizes_user(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 403)

    def test_get_recipe_delete_page_unauthorizes_user(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 403)

    def test_get_recipe_create_page_authorizes_user(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'easy_recipe/recipe_create_form.html')

    # def test_can_add_new_recipe(self):
    #     self.client.login(username='admin', password='adminpassword')
    #     response = self.client.post('/recipe_create_form', {'title': 'Test Added Item',
    #                                 'author':'admin',
    #                                 'content':'test'
    #                                  })
    #     self.assertRedirects(response, reverse('recipe_detail', kwargs=[self.object.id]))

    # def test_can_edit_recipe_item(self):
    #     self.client.login(username='admin', password='adminpassword')
    #     item = RecipePost.objects.create(title='Test Added Item',
    #                                author= User.objects.get(id=current_user.id),
    #                                content='test'
    #                                 )
    #     response = self.client.post(f'/recipe_update_form/{item.id}', {'name': 'Updated Name'})
    #     self.assertRedirects(response, reverse('recipe_detail', kwargs=[item.id]))
    #     update_item = RecipePost.objects.get(id=item.id)
    #     self.assertEqual(update_item.name, 'Updated Name')