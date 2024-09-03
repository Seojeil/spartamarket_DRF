from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_SELECT = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    nickname = models.CharField(max_length=50)
    birth_day = models.DateField()
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    gender = models.CharField(max_length=1, choices=GENDER_SELECT, default='O')
    introduce = models.TextField(null=True)
    
    def __str__(self):
        return self.username
    