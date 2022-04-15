from django.db import models
from vendor import models as vmodel
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class ProductCategory(models.Model):
    name =  models.CharField(max_length=20, null=False)
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=20, null=False)
    price = models.CharField(max_length=20, null=False)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(vmodel.Vendor, on_delete=models.CASCADE, null=True)
    image= models.ImageField(upload_to='product/img/',null=True,blank=True)
    status= models.CharField(max_length=20,default=0)
    description= models.TextField(default='')