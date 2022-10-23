import email
from django.db import models

# Create your models here.
class UsersProf(models.Model):
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)