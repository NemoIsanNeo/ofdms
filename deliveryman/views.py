from django.shortcuts import render
from . import models, forms
from product import models as pmodel

from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test



# Create your views here.


def dman_registration(request):
    userForm = forms.DManUserForm()
    vendorForm = forms.DManForm()
    mydict = {'userForm': userForm, 'vendorForm': vendorForm, 'error': None}
    if request.method == 'POST':
        userForm = forms.DManUserForm(request.POST)
        vendorForm = forms.DManForm(request.POST)
        if userForm.is_valid() and vendorForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            vendor = vendorForm.save(commit=False)
            vendor.user = user
            vendor.save()
            vendor_group = Group.objects.get_or_create(name='DELIVERY')
            vendor_group[0].user_set.add(user)
        return HttpResponseRedirect('/dman/login')
    return render(request, 'delivery/register.html', context=mydict)

def is_dman(user):
    return user.groups.filter(name='DELIVERY').exists()


@login_required(login_url='delivery/login')
@user_passes_test(is_dman)
def dashboard(request):
    dict ={}
    return render(request,'delivery/dashboard.html',context=dict)



@login_required(login_url='vendor/login')
@user_passes_test(is_dman)
def product_details(request):
    product_form = forms.ProductAddForm()
    product = pmodel.Product.objects.all().filter(created_by=models.Vendor.objects.get(user=request.user.id))
    dict ={'product_form':product_form,'product':product}
    if request.method == 'POST':
        product_form = forms.ProductAddForm(request.POST,request.FILES)
        if product_form.is_valid():
            product_details = product_form.save(commit=False)
            product_details.category = pmodel.ProductCategory.objects.get(id=request.POST.get('cat_id'))
            product_details.created_by = models.Vendor.objects.get(user=request.user.id)
            product_details.save()
            return HttpResponseRedirect('/vendor/product-details')            # import pdb; pdb.set_trace()



    return render(request,'vendor/product-details.html',context=dict)


@login_required(login_url='vendor/login')
@user_passes_test(is_dman)
def edit(request, pk):
    instance = pmodel.Product.objects.get(id=pk)
    product_form = forms.ProductAddForm(instance=instance)
    dict = {'product_form': product_form}
    if request.method == 'POST':
        product_form = forms.ProductAddForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_details = product_form.save(commit=False)
            product_details.category = pmodel.ProductCategory.objects.get(id=request.POST.get('cat_id'))
            product_details.created_by = models.Vendor.objects.get(user=request.user.id)
            product_details.save()
            return HttpResponseRedirect('/vendor/product-details')

    return render(request, 'vendor/edit-product.html', context=dict)

