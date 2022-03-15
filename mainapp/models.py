from django.db import models


# Create your models here.
class user_details(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=30)
    password = models.CharField(max_length=15)
    cpass = models.CharField(max_length=15)