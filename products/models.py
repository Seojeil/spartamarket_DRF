from django.db import models
from django.contrib.auth import get_user_model

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
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='products'
        )
    
    def __str__(self):
        return self.title