from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return "{}".format(self.email)


class UserProfile(models.Model):
    display_name = models.CharField(max_length=100,null=True,blank=True)
    phone = models.CharField(unique=True, max_length=20, null=True, blank=True)
    title = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=15, null=True, blank=True)
    active = models.BooleanField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')

    def __str__(self):
        return str(self.display_name)


