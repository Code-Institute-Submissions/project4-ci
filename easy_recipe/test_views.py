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

    def test_get_recipe_detail_page(self):
        self.client.login(username='john', password='johnpassword')
        item = RecipePost.objects.create(title='Test Item',
                                       content='New Item',
                                       author=self.user,
                                       featured_image='')
        response = self.client.get(f'/recipes/recipe_detail/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'easy_recipe/recipe_detail.html')
    
    def test_get_recipe_create_page_unauthorizes_user(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 403)

    def test_get_recipe_edit_page_unauthorizes_user(self):
        self.client.login(username='john', password='johnpassword')
        item = RecipePost.objects.create(title='Test Item',
                                       content='New Item',
                                       author=self.user,
                                       featured_image='')
        response = self.client.get(f'/recipes/recipe_update/{item.id}')
        self.assertEqual(response.status_code, 403)

    def test_get_recipe_delete_page_unauthorizes_user(self):
        self.client.login(username='john', password='johnpassword')
        item = RecipePost.objects.create(title='Test Item',
                                       content='New Item',
                                       author=self.user,
                                       featured_image='')
        response = self.client.get(f'/recipes/recipe_delete/{item.id}')
        self.assertEqual(response.status_code, 403)

    def test_get_recipe_delete_page_authorizes_user(self):
        self.client.login(username='admin', password='adminpassword')
        item = RecipePost.objects.create(title='Test Item',
                                       content='New Item',
                                       author=self.user,
                                       featured_image='')
        response = self.client.get(f'/recipes/recipe_delete/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'easy_recipe/recipe_delete.html')

    def test_get_recipe_create_page_authorizes_user(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('create_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'easy_recipe/recipe_create_form.html')
    

    def test_create_new_recipe(self):
        self.client.login(username='admin', password='adminpassword')
        items = RecipePost.objects.all()
        self.assertEqual(len(items), 0)
        response = self.client.post('/recipes/create_recipe', {'title': 'Recipe',
                                                              'author': self.user.id,
                                                              'content': 'Test',
                                                              'featured_image': ''
                                                              })
        self.assertEqual(response.status_code, 302)                                                     
        new_items = RecipePost.objects.all()
        self.assertEqual(len(new_items), 1)

    def test_get_edit_recipe_item_page(self):
        self.client.login(username='admin', password='adminpassword')
        item = RecipePost.objects.create(title='Test Item',
                                       content='New Item',
                                       author=self.user,
                                       featured_image='')
        response = self.client.get(f'/recipes/recipe_update/{item.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'easy_recipe/recipe_update_form.html')

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

    