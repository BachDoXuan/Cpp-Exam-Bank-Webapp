from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email_confirmed = models.BooleanField(default=False)
#     fullname = models.CharField(max_length=200)
#     address = models.CharField(max_length=50)
#     phone_number = models.CharField(max_length=20)
