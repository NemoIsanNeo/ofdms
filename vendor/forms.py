from django import forms
from django.contrib.auth.models import User
from . import models

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

