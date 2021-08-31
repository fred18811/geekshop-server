from django.test import TestCase
from django.test.client import Client
from products.models import Product, ProductsCategory


class TestMainappSmoke(TestCase):
    def setUp(self):
        self.client = Client()

    def test_products_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/0/')
        self.assertEqual(response.status_code, 200)

        for category in ProductsCategory.objects.all():
            response = self.client.get(f'/products/{category.pk}/')
            self.assertEqual(response.status_code, 200)


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductsCategory.objects.create(name="Штаны")
        self.product_1 = Product.objects.create(name="Штаны 1",
                                                category=category,
                                                price=1999.5,
                                                quantity=44)

        self.product_2 = Product.objects.create(name="Штаны 2",
                                                category=category,
                                                price=2998.1,
                                                quantity=11)

        self.product_3 = Product.objects.create(name="Штаны 3",
                                                category=category,
                                                price=998.1,
                                                quantity=22)

    def test_product_get(self):
        product_1 = Product.objects.get(name="Штаны 1")
        product_2 = Product.objects.get(name="Штаны 2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="Штаны 1")
        product_2 = Product.objects.get(name="Штаны 2")
        self.assertEqual(str(product_1), 'Штаны 1 | Штаны')
        self.assertEqual(str(product_2), 'Штаны 2 | Штаны')