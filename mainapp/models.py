from django.db import models
from django.contrib.auth.models import User
from deliveryman.models import Delivery



class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    mobile = models.CharField(max_length=20, null=False)
    status = models.CharField(max_length=20, null=False, default=0)

    @property
    def get_name(self):
        return self.first_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.first_name + self.last_name




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
    status=models.CharField(max_length=111,default=0)
    payment_type=models.CharField(max_length=111,default=0)
    payment_ref=models.CharField(max_length=111,default=0)
    date=models.CharField(max_length=111,default=0)
    dman = models.ForeignKey(Delivery, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'SI-'+str(self.order_id)