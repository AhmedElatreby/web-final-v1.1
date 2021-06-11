from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from fresher.models import Category, Recipe


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(name='recipe', slug='recipe')

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'recipe')

    def test_category_url(self):
        """
        Test category model slug and URL reverse
        """
        data = self.data1
        response = self.client.post(
            reverse('fresher:category_list', args=[data.slug]))
        self.assertEqual(response.status_code, 200)


class TestRecipesModel(TestCase):
    def setUp(self):
        Category.objects.create(name='recipe', slug='recipe')
        User.objects.create(username='admin')
        self.data1 = Recipe.objects.create(category_id=1, title='recipe beginners', created_by_id=1,
                                        slug='recipe-food', price='20.00', image='recipe')

    def test_recipes_model_entry(self):
        """
        Test recipe model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Recipe))
        self.assertEqual(str(data), 'recipe food')

    def test_recipes_url(self):
        """
        Test recipe model slug and URL reverse
        """
        data = self.data1
        url = reverse('fresher:recipe_detail', args=[data.slug])
        self.assertEqual(url, '/recipe-food')
        response = self.client.post(
            reverse('fresher:recipe_detail', args=[data.slug]))
        self.assertEqual(response.status_code, 200)

    def test_recipes_custom_manager_basic(self):
        """
        Test recipe model custom manager returns only active recipes
        """
        data = Recipe.recipes.all()
        self.assertEqual(data.count(), 1)
