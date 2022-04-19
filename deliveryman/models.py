from django.db import models
from django.contrib.auth.models import User


class Delivery(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20, null=False, default='')
    lastname = models.CharField(max_length=20, null=False, default='')
    mobile = models.CharField(max_length=20, null=False)
    status = models.CharField(max_length=20, null=False, default=0)

    @property
    def get_name(self):
        return self.firstname + self.lastname

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.firstname + self.lastname
