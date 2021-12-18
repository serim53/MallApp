import os.path

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django_markdown.utils import markdown
from markdownx.models import MarkdownxField

# class Tag(models.Model):
#     name = models.CharField(max_length=50,unique=True)
#     slug = models.SlugField(max_length=200,unique=True,allow_unicode=True)
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return f'/blog/tag/{self.slug}'

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/product/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    category = models.ForeignKey(Category,
            null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/images/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', '-updated']
        index_together = [['id', 'slug']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/product/{self.pk}/'

    def get_content_markdown(self):
        return markdown(self.description)

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.product.get_absolute_url()}#comment-{self.pk}'

    def get_avatar_url(self):
        if self.author.socialaccount_set.exists() :
            return self.author.socialaccount_set.first().get_avatar_url()
        else :
            return 'https://doitdjango.com/avatar/id/435/34def6c20b3733a7/svg/{self.author.email}/'
