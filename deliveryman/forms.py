from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.models import User
from . import models
from mainapp.models import Orders
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



class DtDmanForm(forms.ModelForm):
    dman_id = forms.ModelChoiceField(queryset=models.Delivery.objects.all(), empty_label="Delivery Man", to_field_name="id")
    order_id = forms.ModelChoiceField(queryset=Orders.objects.all(), empty_label="Order", to_field_name="order_id")
    class Meta:
        model=Orders
        fields=['dman_id','order_id']