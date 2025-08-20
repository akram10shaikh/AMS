from django.contrib import admin
from django.core.validators import EmailValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings


# Extend the User model to identify super admins
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('SuperAdmin', 'Super Admin'),
        ('OrganizationAdmin', 'Organization Admin'),
        ('Staff', 'Staff'),
        ('Player', 'Player'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='SuperAdmin')
    is_super_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Automatically set is_super_admin to True if role is SuperAdmin, otherwise False
        if self.role == 'SuperAdmin':
            self.is_super_admin = True
        else:
            self.is_super_admin = False
        super().save(*args, **kwargs)


class Organization(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    role = models.CharField(max_length=20, default='OrganizationAdmin')

    def __str__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()

    # Permissions
    player_management = models.BooleanField(default=False)
    injury_tracking = models.BooleanField(default=False)
    add_form = models.BooleanField(default=False)
    add_result = models.BooleanField(default=False)
    view_result = models.BooleanField(default=False)
    create_camps_tournaments = models.BooleanField(default=False)  # Permission to create camps/tournaments
    view_camps_tournaments = models.BooleanField(default=False)  # Permission to view camps/tournaments
    create_program = models.BooleanField(default=False)  # Permission to create programs
    assign_program = models.BooleanField(default=False)  # Permission to assign programs
    view_programs = models.BooleanField(default=False)  # Permission to view programs

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default='Staff')

    def __str__(self):
        return self.name


