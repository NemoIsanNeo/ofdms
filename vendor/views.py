from django.shortcuts import render

from deliveryman.forms import DtDmanForm
from . import models, forms
from product import models as pmodel
from mainapp import models as mmodel

from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
import json
from deliveryman import models as dmodel




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


@login_required(login_url='vendor/login')
@user_passes_test(is_vendor)
def dashboard(request):
    product = pmodel.Product.objects.all().filter(created_by=models.Vendor.objects.get(user=request.user.id)).count()
    p_product = pmodel.Product.objects.all().filter(created_by=models.Vendor.objects.get(user=request.user.id), status=0).count()


    dict ={'product':product, 'p_product':p_product}
    return render(request,'vendor/dashboard.html',context=dict)



@login_required(login_url='vendor/login')
@user_passes_test(is_vendor)
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
@user_passes_test(is_vendor)
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




@login_required(login_url='vendor/login')
@user_passes_test(is_vendor)
def product_orders(request):
    dtoform = DtDmanForm()
    order = mmodel.Orders.objects.all().filter()
    dict = {'order': order,'dtoform':dtoform}
    datalist = []

    for j in order:
        item = json.loads(j.items_json)

        subtotal = 0
        qty = 0
        qty2 = 0
        for i in item:
            id = i.split("pr")[1]
            qty1 = item[i][0]
            price = pmodel.Product.objects.get(id=id).price
            total = int(qty1) * int(price)
            name = pmodel.Product.objects.get(id=id).name
            vendor = pmodel.Product.objects.get(id=id).created_by
            if vendor == models.Vendor.objects.get(user_id=request.user.pk):
                datadict = {
                    'order_no': j.order_id,
                    'product_name': name,
                    'qty': qty1,
                    'total': total,
                    'date': j.date,
                    'status': 'Pending' if j.status == '0' else 'Delivered',
                    'dman': j.dman,
                }
                datalist.append(datadict)


    dict.update({'datalist': datalist})

    if request.POST:
        order_form = DtDmanForm(request.POST)
        if order_form.is_valid():
            order = models.Orders.objects.get(order_id=request.POST.get('order_id'))
            order.dman = dmodel.Delivery.objects.get(id=request.POST.get('dman_id'))
            order.save()


    return render(request,'vendor/order-details.html',context=dict)


