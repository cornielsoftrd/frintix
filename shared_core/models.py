from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class Company(models.Model):
    """Restaurante registrado en la plataforma."""
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, company=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, company=company, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, company=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        
        return self._create_user(email, password, company=company, **extra_fields)

    def create_superuser(self, email, password=None, company=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, company=company, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('restaurant_admin', 'Restaurant Admin'),
        ('business_admin', 'Business Admin'),
        ('employee', 'Employee'),
        ('retail_customer', 'Retail Customer'),
    )
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)  # obligatorio para AbstractUser
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)  # Solo restaurant_admin tiene company asignada
    
    is_businessadmin=models.BooleanField(default=False)
    is_tenantadmin=models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
