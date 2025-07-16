from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone', 'city']

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',
        blank=True,
    )
