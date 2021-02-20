from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.core.cache import cache
from django.conf import settings

import os
from shutil import copy


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def categories_cache_clear(sender, **kwargs):
    cache.delete('categories_list')


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)
    description = models.TextField(max_length=1000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    image = models.ImageField(blank=True, upload_to='products')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


#  Attempt to avoid heroku media files trouble

#     def static_image(self):
#         if self.image:
#             path = os.path.join('img', self.image.name.split('/')[1])
#             return path
#
#
# @receiver(post_save, sender=Product)
# def media_image_to_static(sender, instance, **kwargs):
#     path = instance.image.path
#     name = path.split('/')[-1]
#     copy(path, os.path.join(settings.BASE_DIR, f'static/img/{name}'))


class SpecificationsItem(models.Model):
    product = models.ForeignKey(Product, related_name='specs', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
