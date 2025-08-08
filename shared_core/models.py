from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

class Company(models.Model):
    """Represents a Restaurant in the public schema."""
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('restaurant_admin', 'Restaurant Admin'),
        ('business_admin', 'Business Admin'),
        ('employee', 'Employee'),
    )
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)  # keep but optional
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    # note: business_client relation is per-tenant — see business.Employee below (links to user)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
