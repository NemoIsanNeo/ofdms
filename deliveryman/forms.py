from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.models import User
from . import models
from product import models as pmodel
class DManUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class DManForm(forms.ModelForm):
    class Meta:
        model=models.Delivery
        fields=['mobile','firstname','lastname']



