from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    category = models.CharField(max_length=50, unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    price = models.PositiveIntegerField()
    image = models.ImageField(
        upload_to='images/',
        blank=True,
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
        )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='products'
        )
    like_users = models.ManyToManyField(
        get_user_model(),
        related_name='like_products',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='products',
        blank=True,
        null=True,
    )
    
    def __str__(self):
        return self.title