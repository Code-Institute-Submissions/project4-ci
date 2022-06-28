from django.test import TestCase
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from .models import RecipePost


class TestViews(TestCase):
    """
    Tests for all the view in the Easy_recipe app.
    Tests to get pages delete, edit and create items in the
    database
    """

    def setUp(self):
        """
        Setup users with different status
        """
        self.client = Client()
        self.user = User.objects.create_user('john',
                                             'lennon@thebeatles.com',
                                             'johnpassword')
        self.user = User.objects.create_superuser('admin',
                                                  'admin@mail.com',
                                                  'adminpassword')

    def test_get_recipe_list_page_authorized_user(self):
        """
        Function to get recipes page if logged in
        """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'easy_recipe/recipes.html')

    def test_get_recipe_list_page_not_loggedin(self):
        """
        Function to get recipes page if not logged in
        """
        response = self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/recipes/')

    def test_get_recipe_detail_page(self):
        """
        Function to get recipes detail page
        """
        self.client.login(username='john', password='johnpassword')
        item = RecipePost.objects.create(title='Test Item',
                                         content='New Item',
                                         author=self.user,
                                         featured_image='')
        response = self.client.get(f'/recipes/recipe_detail/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'easy_recipe/recipe_detail.html')

    def test_get_recipe_create_page_unauthorizes_user(self):
        """
        Function to get recipes create page if not staff
        """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 403)

    def test_get_recipe_edit_page_unauthorizes_user(self):
        """
        Function to get recipes edit page if not staff
        """
        self.client.login(username='john', password='johnpassword')
        item = RecipePost.objects.create(title='Test Item',
                                         content='New Item',
                                         author=self.user,
                                         featured_image='')
        response = self.client.get(f'/recipes/recipe_update/{item.id}')
        self.assertEqual(response.status_code, 403)

    def test_get_recipe_delete_page_unauthorizes_user(self):
        """
        Function to get recipes delete page if not staff
        """
        self.client.login(username='john', password='johnpassword')
        item = RecipePost.objects.create(title='Test Item',
                                         content='New Item',
                                         author=self.user,
                                         featured_image='')
        response = self.client.get(f'/recipes/recipe_delete/{item.id}')
        self.assertEqual(response.status_code, 403)

    def test_get_recipe_delete_page_authorizes_user(self):
        """
        Function to get recipes delete page if staff
        """
        self.client.login(username='admin', password='adminpassword')
        item = RecipePost.objects.create(title='Test Item',
                                         content='New Item',
                                         author=self.user,
                                         featured_image='')
        response = self.client.get(f'/recipes/recipe_delete/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'easy_recipe/recipe_delete.html')

    def test_get_recipe_create_page_authorizes_user(self):
        """
        Function to get recipes create page if staff
        """
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'easy_recipe/recipe_create_form.html')

    def test_create_new_recipe(self):
        """
        Function to test if authorized user can create new recipe post
        """
        self.client.login(username='admin', password='adminpassword')
        items = RecipePost.objects.all()
        self.assertEqual(len(items), 0)
        response = self.client.post('/recipes/create_recipe',
                                    {'title': 'Recipe',
                                     'author': self.user.id,
                                     'content': 'Test',
                                     'featured_image': ''})
        self.assertEqual(response.status_code, 302)
        new_items = RecipePost.objects.all()
        self.assertEqual(len(new_items), 1)

    def test_get_edit_recipe_item_page(self):
        """
        Function to get recipes edit page if staff
        """
        self.client.login(username='admin', password='adminpassword')
        item = RecipePost.objects.create(title='Test Item',
                                         content='New Item',
                                         author=self.user,
                                         featured_image='')
        response = self.client.get(f'/recipes/recipe_update/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'easy_recipe/recipe_update_form.html')

    def test_delete_recipe(self):
        """Function to check whether a recipe can be deleted."""
        self.client.login(username='admin', password='adminpassword')
        item = RecipePost.objects.create(title='Test Item',
                                         content='New Item',
                                         author=self.user,
                                         featured_image='')
        existing_items = RecipePost.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 1)
        response = self.client.post(f'/recipes/recipe_delete/{item.id}')
        self.assertEqual(response.status_code, 302)
        existing_items = RecipePost.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 0)

    def test_edit_recipe(self):
        """Function to check whether a menu item can be updated."""
        self.client.login(username='admin', password='adminpassword')
        item = RecipePost.objects.create(title='Test Item',
                                         content='New Item',
                                         author=self.user,
                                         featured_image='')
        response = self.client.post(f'/recipes/recipe_update/{item.id}',
                                    {
                                        'title': 'Test Edit Item check',
                                        'content': 'New Item',
                                        'author': self.user.id,
                                        'featured_image': '',
                                    })
        self.assertEqual(response.status_code, 302)
        updated_item = RecipePost.objects.get(id=item.id)
        self.assertEqual(updated_item.title, 'Test Edit Item check')
