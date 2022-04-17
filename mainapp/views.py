from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

from mainapp.models import Orders
from . import models
from product import models as pmodel
from vendor import forms as vfrom
from vendor import models as vmodel
from . import forms
from django.contrib.auth.models import User , Group



# Create your views here.

def index(request):
    product =  pmodel.Product.objects.all().filter(status=1)
    dict = {'product':product}
    if is_vendor(request.user):
        return redirect('vendor/dashboard')

    return render(request, 'index.html',context=dict)







def register(request):
    userForm = forms.GUserForm()
    gfrom = forms.GForm()
    mydict = {'userForm': userForm, 'gfrom': gfrom, 'error': None}
    if request.method == 'POST':
        userForm = forms.GUserForm(request.POST)
        gfrom = forms.GForm(request.POST)
        if userForm.is_valid() and gfrom.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            vendor = gfrom.save(commit=False)
            vendor.user = user
            vendor.save()
            vendor_group = Group.objects.get_or_create(name='GUEST')
            vendor_group[0].user_set.add(user)
        return HttpResponseRedirect('/login')
    return render(request, 'register.html', context=mydict)


def account(request):
    return render(request, 'account.html')


def cart_details(request):
    return render(request, 'cart_details.html')


def checkout(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            items_json = request.POST.get('itemsJson')
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address1') + " " + request.POST.get('address2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip_code = request.POST.get('zip_code')
            phone = request.POST.get('phone')

            order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                           zip_code=zip_code, phone=phone)

            order.order_by = models.Users.objects.get(user=request.user.id)
            order.save()
            thank = True
            id = order.order_id
            return render(request, 'checkout.html', {'thank': thank, 'id': id})
        return render(request, 'checkout.html')
    else:
        return redirect("login")







def food_list(request):
    return render(request, 'food_list.html')


def food_details(request):
    return render(request, 'food_details.html')

from django.shortcuts import render,redirect,reverse



def is_vendor(user):
    return user.groups.filter(name='VENDOR').exists()

def is_guest(user):
    return user.groups.filter(name='GUEST').exists()



def afterlogin_view(request):
    if is_vendor(request.user):
        vendor = vmodel.Vendor.objects.get(user=request.user.id)
        if vendor.status == '1':
            return HttpResponseRedirect('vendor/dashboard')
        else:
            return redirect('logout')

    elif is_guest(request.user):
        return redirect('/')

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
