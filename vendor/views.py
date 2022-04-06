from django.shortcuts import render
from . import models, forms
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test



# Create your views here.


def vendor_register(request):
    userForm = forms.VendorUserForm()
    vendorForm = forms.VendorForm()
    mydict = {'userForm': userForm, 'vendorForm': vendorForm, 'error': None}
    if request.method == 'POST':
        userForm = forms.VendorUserForm(request.POST)
        vendorForm = forms.VendorForm(request.POST)
        if userForm.is_valid() and vendorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            vendor = vendorForm.save(commit=False)
            vendor.user = user
            vendor.save()
            vendor_group = Group.objects.get_or_create(name='VENDOR')
            vendor_group[0].user_set.add(user)
        return HttpResponseRedirect('/vendor/login')
    return render(request, 'vendor/register.html', context=mydict)

def is_vendor(user):
    return user.groups.filter(name='VENDOR').exists()


@login_required(login_url='studentlogin')
@user_passes_test(is_vendor)
def dashboard(request):
    dict ={}
    return render(request,'vendor/dashboard.html',context=dict)

