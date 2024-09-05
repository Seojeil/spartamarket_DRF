from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
    )


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        extra_fields.setdefault('nickname', 'Admin')
        extra_fields.setdefault('birth_day', '2000-01-01')
        extra_fields.setdefault('first_name', 'Ad')
        extra_fields.setdefault('last_name', 'Min')
        return self._create_user(username, email, password, **extra_fields)


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
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username