from django.db import models
from django.contrib.auth.models import User


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
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




class Orders(models.Model):
    order_by = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    order_id= models.AutoField(primary_key=True)
    items_json= models.CharField(max_length=5000)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111)
    phone=models.CharField(max_length=111)