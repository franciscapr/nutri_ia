from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserProfile(models.Model):
    # Enlace al usuario estándar de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Datos nutricionales y físicos
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=[('male', 'Hombre'), ('female', 'Mujer'), ('other', 'Otro')])
    height_cm = models.PositiveIntegerField(null=True, blank=True)  # altura en cm
    weight_kg = models.FloatField(null=True, blank=True)
    tmb = models.FloatField(null=True, blank=True, help_text="Tasa metabólica basal")

    # Rol futuro
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('nutritionist', 'Nutricionista'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')



class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)


    # Campos por defecto django
    date_joined = models.DateTimeField(auto_now_add=True)
    date_login = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
