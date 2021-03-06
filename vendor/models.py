from django.db import models
from django.contrib.auth.models import User


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=20, null=False)
    mobile = models.CharField(max_length=20, null=False)
    status = models.CharField(max_length=20, null=False, default=0)

    @property
    def get_name(self):
        return self.company_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.company_name
