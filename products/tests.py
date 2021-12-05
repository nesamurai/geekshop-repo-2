from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from products.models import Product, ProductCategory

# Create your tests here.
class TestProductsSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_products_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/category/1/')
        self.assertEqual(response.status_code, 200)
