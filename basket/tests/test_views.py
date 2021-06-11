from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from fresher.models import Category, Recipe


class TestBasketView(TestCase):
    def setUp(self):
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Recipe.objects.create(category_id=1, title='django beginners', created_by_id=1,
                        slug='django-beginners', price='20.00', image='django')
        Recipe.objects.create(category_id=1, title='django intermediate', created_by_id=1,
                        slug='django-beginners', price='20.00', image='django')
        Recipe.objects.create(category_id=1, title='django advanced', created_by_id=1,
                        slug='django-beginners', price='20.00', image='django')
        self.client.post(
            reverse('basket:basket_add'), {"recipeid": 1, "recipeqty": 1, "action": "post"}, xhr=True)
        self.client.post(
            reverse('basket:basket_add'), {"recipeid": 2, "recipeqty": 2, "action": "post"}, xhr=True)

    def test_basket_url(self):
        """
        Test homepage response status
        """
        response = self.client.get(reverse('basket:basket_summary'))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Test adding items to the basket
        """
        response = self.client.post(
            reverse('basket:basket_add'), {"recipeid": 3, "recipeqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 4})
        response = self.client.post(
            reverse('basket:basket_add'), {"recipeid": 2, "recipeqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 3})

    def test_basket_delete(self):
        """
        Test deleting items from the basket
        """
        response = self.client.post(
            reverse('basket:basket_delete'), {"recipeid": 2, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 1, 'subtotal': '20.00'})

    def test_basket_update(self):
        """
        Test updating items from the basket
        """
        response = self.client.post(
            reverse('basket:basket_update'), {"recipeid": 2, "recipeqty": 1, "action": "post"}, xhr=True)
        self.assertEqual(response.json(), {'qty': 2, 'subtotal': '40.00'})
