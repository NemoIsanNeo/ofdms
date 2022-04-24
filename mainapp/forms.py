from django import forms
from django.contrib.auth.models import User
from . import models
from product import models as pmodel
class GUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class GForm(forms.ModelForm):
    class Meta:
        model=models.Users
        fields=['mobile','first_name','last_name','address']