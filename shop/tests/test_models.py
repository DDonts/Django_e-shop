from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from shop import models


def sample_user(username='SampleUser', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(username, password)


def sample_category(title='Category', slug='category'):
    return models.Category.objects.create(title=title, slug=slug)


def sample_product(category, title='Product', slug='product', description='test product', price=999.99):
    return models.Product.objects.create(category=category, title=title, slug=slug, description=description, price=price)


def sample_specification(product, name='specification', value='value'):
    return models.SpecificationsItem.objects.create(product=product, name=name, value=value)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        username = 'SampleUser'
        password = 'testpass'
        user = get_user_model().objects.create_user(username=username, password=password)

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_username(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        user = get_user_model().objects.create_superuser('SampleUser', 'test123')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_product_str(self):
        """Tes the product representation"""
        category = sample_category()
        product = sample_product(category)

        self.assertEqual(str(product), product.title)

    def test_category_str(self):
        """Test the category string representation"""
        category = sample_category()

        self.assertEqual(str(category), category.title)

    def test_specification_str(self):
        """Test the specification string representation"""
        category = sample_category()
        product = sample_product(category)
        specification = sample_specification(product)

        self.assertEqual(str(specification), specification.name)


