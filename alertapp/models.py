from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Alert(models.Model):
    STATUS_CHOICES = [
        ("created", "Created"),
        ("triggered", "Triggered"),
        ("deleted", "Deleted"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    target_price = models.DecimalField(max_digits=20, decimal_places=2)
    current_price = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.item} Alert"
