from django import forms
from django.contrib.auth.models import User
from . import models
from product import models as pmodel
class VendorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class VendorForm(forms.ModelForm):
    class Meta:
        model=models.Vendor
        fields=['mobile','company_name']



class ProductAddForm(forms.ModelForm):
    cat_id = forms.ModelChoiceField(queryset=pmodel.ProductCategory.objects.all(), empty_label="Category Name",to_field_name="id")

    class Meta:
        model = pmodel.Product
        fields = ['name','price','image']