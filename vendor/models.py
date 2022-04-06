from django.db import models
from django.contrib.auth.models import User


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=20, null=False)
    mobile = models.CharField(max_length=20, null=False)

    @property
    def get_name(self):
        return self.user

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user
