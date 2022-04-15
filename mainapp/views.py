from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from . import models
from product import models as pmodel
from vendor import forms as vfrom
from vendor import models as vmodel
from django.contrib.auth.models import User



# Create your views here.

def index(request):
    product =  pmodel.Product.objects.all().filter(status=1)
    dict = {'product':product}
    if is_vendor(request.user):
        return redirect('vendor/dashboard')

    return render(request, 'index.html',context=dict)


def login(request):
    return render(request, 'login.html')


def register(request):
    userdata = models.user_details()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        cpass = request.POST.get('cpass')

        if name and email and phone and address and password and cpass:
            userdata.name = name
            userdata.email = email
            userdata.phone = phone
            userdata.address = address
            userdata.password = password
            userdata.cpass = cpass
            userdata.save()
        else:
            print('Nothing')
    return render(request, 'register.html')


def account(request):
    return render(request, 'account.html')


def cart_details(request):
    return render(request, 'cart_details.html')


def checkout(request):
    return render(request, 'checkout.html')


def food_list(request):
    return render(request, 'food_list.html')


def food_details(request):
    return render(request, 'food_details.html')

from django.shortcuts import render,redirect,reverse



def is_vendor(user):
    return user.groups.filter(name='VENDOR').exists()



def afterlogin_view(request):
    if is_vendor(request.user):
        vendor = vmodel.Vendor.objects.get(user=request.user.id)
        if vendor.status == '1':
            return HttpResponseRedirect('vendor/dashboard')
        else:
            return redirect('logout')


    # elif is_teacher(request.user):
    #     if request.POST:
    #         verifyno = TMODEL.Teacher.objects.filter(user_id=request.user.id).values('verification')
    #         verifydata = verifyno[0]['verification']
    #         if str(request.POST['verifynumber']) == str(verifydata):
    #             teacherm = TMODEL.Teacher.objects.get(user_id=request.user.id)
    #             teacherm.verify_state = 1
    #             teacherm.save()
    #             accountapproval = TMODEL.Teacher.objects.all().filter(user_id=request.user.id, status=True, )
    #             if accountapproval:
    #                 return redirect('teacher/teacher-dashboard')
    #             else:
    #                 return render(request, 'teacher/teacher_wait_for_approval.html')
    #         else:
    #             return render(request, 'teacher/verify.html')
    #     accountapproval = TMODEL.Teacher.objects.all().filter(user_id=request.user.id, status=True, )
    #     if accountapproval:
    #         return redirect('teacher/teacher-dashboard')
    #     else:
    #         verify = TMODEL.Teacher.objects.all().filter(user_id=request.user.id, verify_state=0)
    #         if verify:
    #             return render(request, 'teacher/verify.html')
    #         else:
    #           return render(request, 'teacher/teacher_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



def admin_dashboard_view(request):
    dict = {}

    return render(request,'admin/dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def cat_details(request):
    cat_form = vfrom.ProductCatAddForm()
    product_cat = pmodel.ProductCategory.objects.all()
    dict ={'cat_form':cat_form,'product':product_cat}
    if request.method == 'POST':
        product_cat = vfrom.ProductCatAddForm(request.POST)
        if product_cat.is_valid():
            product_cat = product_cat.save(commit=False)
            product_cat.save()
            return HttpResponseRedirect('/sadmin/product-category/')
    return render(request, 'admin/cat-details.html',context=dict)

@login_required(login_url='adminlogin')
def delete_product_category(request, pk):
    product_cat =  pmodel.ProductCategory.objects.get(id=pk)
    product_cat.delete()
    return HttpResponseRedirect('/sadmin/product-category')  # import pdb; pdb.set_trace()

@login_required(login_url='adminlogin')
def product_details(request):
    product_form = vfrom.ProductAddForm()
    product = pmodel.Product.objects.all()
    dict ={'product_form':product_form,'product':product}
    if request.method == 'POST':
        product_form = vfrom.ProductAddForm(request.POST,request.FILES)
        if product_form.is_valid():
            product_details = product_form.save(commit=False)
            product_details.category = pmodel.ProductCategory.objects.get(id=request.POST.get('cat_id'))
            product_details.save()
            return HttpResponseRedirect('/sadmin/product-details')            # import pdb; pdb.set_trace()



    return render(request,'admin/product-details.html',context=dict)


@login_required(login_url='adminlogin')
def vendor(request):
    vendor = vmodel.Vendor.objects.all()
    dict ={'vendor':vendor}

    return render(request,'admin/vendor.html',context=dict)



@login_required(login_url='adminlogin')
def accept_product(request, pk):
    product =  pmodel.Product.objects.get(id=pk)
    product.status = 1
    product.save()
    return HttpResponseRedirect('/sadmin/product-details')  # import pdb; pdb.set_trace()


@login_required(login_url='adminlogin')
def reject_product(request, pk):
    product =  pmodel.Product.objects.get(id=pk)
    product.status = 2
    product.save()
    return HttpResponseRedirect('/sadmin/product-details')  # import pdb; pdb.set_trace()



@login_required(login_url='adminlogin')
def delete_product(request, pk):
    product =  pmodel.Product.objects.get(id=pk)
    product.delete()
    return HttpResponseRedirect('/sadmin/product-details')  # import pdb; pdb.set_trace()









@login_required(login_url='adminlogin')
def accept_vendor(request, pk):

    vendor =  vmodel.Vendor.objects.get(id=pk)
    vendor.status = 1
    vendor.save()
    return HttpResponseRedirect('/sadmin/vendor')  # import pdb; pdb.set_trace()


@login_required(login_url='adminlogin')
def reject_vendor(request, pk):
    vendor =  vmodel.Vendor.objects.get(id=pk)
    vendor.status = 2
    vendor.save()
    return HttpResponseRedirect('/sadmin/vendor')  # import pdb; pdb.set_trace()

@login_required(login_url='adminlogin')
def delete_vendor(request, pk):
    vendor =  vmodel.Vendor.objects.get(id=pk)
    vendor.delete()
    return HttpResponseRedirect('/sadmin/vendor')  # import pdb; pdb.set_trace()
