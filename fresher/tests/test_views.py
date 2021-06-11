from importlib import import_module
from unittest import skip

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from fresher.models import Category, Recipe
from fresher.views import recipe_all


@skip("demonstrating skipping")
class TestSkip(TestCase):
    def test_skip_exmaple(self):
        pass


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        User.objects.create(username='admin')
        Category.objects.create(name='recipe', slug='recipe')
        Recipe.objects.create(category_id=1, title='recipe food', created_by_id=1,
                            slug='recipe-food', price='20.00', image='recipe')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)

    def test_homepage_url(self):
        """
        Test homepage response status
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_url(self):
        """
        Test category response status
        """
        response = self.c.get(
            reverse('fresher:category_list', args=['recipe']))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_url(self):
        """
        Test items response status
        """
        response = self.c.get(
            reverse('fresher:recipe_detail', args=['recipe-food']))
        self.assertEqual(response.status_code, 200)

    def test_homepage_html(self):
        """
        Example: code validation, search HTML for text
        """
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.Sessionfresher()
        response = recipe_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Fresher</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
