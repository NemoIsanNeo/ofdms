from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

from deliveryman.forms import DtDmanForm
from mainapp.models import Orders
from . import models
from product import models as pmodel
from vendor import forms as vfrom
from vendor import models as vmodel
from deliveryman import models as dmodel
from . import forms
from django.contrib.auth.models import User , Group
from django.contrib import messages
import json

from io import BytesIO #A stream implementation using an in-memory bytes buffer
                       # It inherits BufferIOBase

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()

    #This part will create the pdf.
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# Create your views here.

def index(request):
    product =  pmodel.Product.objects.all().filter(status=1)
    category = pmodel.ProductCategory.objects.all()

    dict = {'product':product,'category':category}
    if is_vendor(request.user):
        vendor = vmodel.Vendor.objects.get(user=request.user.id)
        if vendor.status == '1':
            try:
                del request.session['mykey']
            except:
                pass
            request.session['name'] = vendor.company_name
            return redirect('vendor/dashboard')

    elif is_dman(request.user):
        dman = dmodel.Delivery.objects.get(user=request.user.id)
        if dman.status == '1':
            try:
                del request.session['mykey']
            except:
                pass
            request.session['name'] = dman.firstname + dman.lastname
            return redirect('dman/dashboard')

    elif is_guest(request.user):
        user = models.Users.objects.get(user=request.user.id)
        try:
            del request.session['name']
        except:
            pass
        request.session['name'] = user.first_name+ " " + user.last_name

        return render(request, 'index.html', context=dict)

    return render(request, 'index.html',context=dict)


def order(request):
    order = models.Orders.objects.all().filter(order_by=models.Users.objects.get(user=request.user.id))
    dict = {'order':order}
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
            qty = qty + 1
            qty2 += qty1

            subtotal = subtotal + total

        if j.status == '0':
            status = 'Pending'
        elif j.status == '1':
            status = 'Picked Up'
        elif j.status == '2':
            status = 'Rejected'
        else:
            status = 'Delivered'

        datadict = {
            'order_no': j.order_id,
            'item': qty,
            'qty':qty2,
            'total': subtotal,
            'date':j.date,
            'status': status
        }
        datalist.append(datadict)
    dict.update({'datalist':datalist})

    return render(request, 'order.html',context=dict)








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


@login_required(login_url='login')
def account(request):
    if is_guest(request.user):
        user = models.Users.objects.get(user=request.user.id)

        userForm = forms.GUserForm(instance=request.user)
        gfrom = forms.GForm(instance=user)
        mydict = {'userForm': userForm, 'gfrom': gfrom, 'error': None,'user': user}
        if request.method == 'POST':
            gfrom = forms.GForm(request.POST, instance=request.user.users)
            if gfrom.is_valid():
                gfrom.save()
            return HttpResponseRedirect('/account')

        return render(request, 'account.html', context=mydict)

    else:
        redirect('index')



def cart_details(request):
    return render(request, 'cart_details.html')


def checkout(request):
    error = ''
    category = pmodel.ProductCategory.objects.all()
    dict = {'category':category}
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
            payment = request.POST.get('payment')
            bkash_ref = request.POST.get('bkash_ref')

            order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state,
                           zip_code=zip_code, phone=phone)

            order.order_by = models.Users.objects.get(user=request.user.id)
            from datetime import date
            today = date.today()
            order.date =  today
            if payment == '2':
                if bkash_ref != '':
                    order.payment_type = payment
                    order.payment_ref = bkash_ref
                else:
                    error = 'please give ref number'
                    dict.update({'error':error})
                    return render(request, 'checkout.html', context=dict)
            elif payment == '1':
                order.payment_type = payment

            else:
                error = 'Please select payment option'
                dict.update({'error': error})
                return render(request, 'checkout.html',context=dict)

            order.save()
            thank = True
            id = order.order_id
            dict.update({'thank': thank, 'id': id,'error':error})
            return render(request, 'checkout.html',context=dict )

        return render(request, 'checkout.html',context=dict)
    else:
        return redirect("login")







def food_list(request,pk):
    cat = True

    product =  pmodel.Product.objects.all().filter(status=1,category=pk)
    category = pmodel.ProductCategory.objects.all()

    dict = {'product':product,'category':category,'cat':cat}
    if is_vendor(request.user):
        vendor = vmodel.Vendor.objects.get(user=request.user.id)
        if vendor.status == '1':
            try:
                del request.session['mykey']
            except:
                pass
            request.session['name'] = vendor.company_name
            return redirect('vendor/dashboard')

    elif is_dman(request.user):
        dman = dmodel.Delivery.objects.get(user=request.user.id)
        if dman.status == '1':
            try:
                del request.session['mykey']
            except:
                pass
            request.session['name'] = dman.firstname + dman.lastname
            return redirect('dman/dashboard')

    elif is_guest(request.user):
        user = models.Users.objects.get(user=request.user.id)
        try:
            del request.session['name']
        except:
            pass
        request.session['name'] = user.first_name+ " " + user.last_name

        return render(request, 'index.html', context=dict)

    return render(request, 'index.html',context=dict)



def food_details(request):
    return render(request, 'food_details.html')

from django.shortcuts import render,redirect,reverse



def is_vendor(user):
    return user.groups.filter(name='VENDOR').exists()

def is_dman(user):
    return user.groups.filter(name='DELIVERY').exists()

def is_guest(user):
    return user.groups.filter(name='GUEST').exists()



def afterlogin_view(request):
    if is_vendor(request.user):
        vendor = vmodel.Vendor.objects.get(user=request.user.id)
        if vendor.status == '1':
            return HttpResponseRedirect('vendor/dashboard')
        else:
            return render(request,'vendor/login.html',{'error':"Wait for admin approval......."})

    if is_dman(request.user):
        dman = dmodel.Delivery.objects.get(user=request.user.id)
        if dman.status == '1':
            return HttpResponseRedirect('dman/dashboard')
        else:
            return HttpResponseRedirect('logout')

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
    vendor = vmodel.Vendor.objects.all().count()
    dman = dmodel.Delivery.objects.all().count()
    order = models.Orders.objects.all().count()

    dict = {'vendor':vendor,'dman':dman,'order':order}

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
def product_orders(request):
    dtoform = DtDmanForm()
    order = models.Orders.objects.all()
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
            qty = qty + 1
            qty2 += qty1

            subtotal = subtotal + total
        datadict = {
            'order_no': j.order_id,
            'item': qty,
            'qty': qty2,
            'total': subtotal,
            'date': j.date,
            'status': 'Pending' if j.status == '0' else 'Delivered',
            'dman':j.dman,
            'ptype': 'Cash On' if j.payment_type == '1' else 'Bkash',
            'pref': j.payment_ref if j.payment_ref !='0' else 'No Bkash'
        }
        datalist.append(datadict)
    dict.update({'datalist': datalist})

    if request.POST:
        order_form = DtDmanForm(request.POST)
        if order_form.is_valid():
            order = models.Orders.objects.get(order_id=request.POST.get('order_id'))
            order.dman = dmodel.Delivery.objects.get(id=request.POST.get('dman_id'))
            order.save()


    return render(request,'admin/order-details.html',context=dict)



@login_required(login_url='adminlogin')
def orders_report(request):
    dtoform = DtDmanForm()
    order = models.Orders.objects.all()
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
            qty = qty + 1
            qty2 += qty1

            subtotal = subtotal + total

        if j.status == '0':
            status = 'Pending'
        elif j.status == '1':
            status = 'Picked Up'
        elif j.status == '2':
            status = 'Rejected'
        else:
            status = 'Delivered'

        datadict = {
            'order_no': j.order_id,
            'item': qty,
            'qty': qty2,
            'total': subtotal,
            'date': j.date,
            'status': status,
            'dman':j.dman
        }
        datalist.append(datadict)
    dict.update({'datalist': datalist})

    if request.POST:
        import datetime
        from_date = request.POST.get('from') if request.POST.get('from') else str(datetime.datetime.today().strftime('%Y-%m-%d'))
        to_date = request.POST.get('to') if request.POST.get('to') else str(datetime.datetime.today().strftime('%Y-%m-%d'))
        order =models.Orders.objects.all().filter(date__gte=from_date, date__lte=to_date)
        dict = {'order': order, 'dtoform': dtoform}
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
                qty = qty + 1
                qty2 += qty1

                subtotal = subtotal + total
            datadict = {
                'order_no': j.order_id,
                'item': qty,
                'qty': qty2,
                'total': subtotal,
                'date': j.date,
                'status': 'Pending' if j.status == '0' else 'Delivered',
                'dman': j.dman
            }
            datalist.append(datadict)
        dict.update({'datalist': datalist})

        if request.POST.get('print'):
            return render_to_pdf('admin/pdf.html',context_dict=dict)
        else:
            return render(request, 'admin/orders-report.html', context=dict)

    return render(request,'admin/orders-report.html',context=dict)


@login_required(login_url='adminlogin')
def vendor(request):
    vendor = vmodel.Vendor.objects.all()
    dict ={'vendor':vendor}

    return render(request,'admin/vendor.html',context=dict)

@login_required(login_url='adminlogin')
def dman_details(request):
    dman = dmodel.Delivery.objects.all()
    dict ={'vendor':dman}

    return render(request,'admin/delivery.html',context=dict)



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



@login_required(login_url='adminlogin')
def accept_dman(request, pk):

    dman =  dmodel.Delivery.objects.get(id=pk)
    dman.status = 1
    dman.save()
    return HttpResponseRedirect('/sadmin/dman')  # import pdb; pdb.set_trace()


@login_required(login_url='adminlogin')
def reject_dman(request, pk):
    dman = dmodel.Delivery.objects.get(id=pk)
    dman.status = 2
    dman.save()
    return HttpResponseRedirect('/sadmin/dman')  # import pdb; pdb.set_trace()

@login_required(login_url='adminlogin')
def delete_dman(request, pk):
    dman = dmodel.Delivery.objects.get(id=pk)
    dman.delete()
    return HttpResponseRedirect('/sadmin/dman')  # import pdb; pdb.set_trace()


@login_required(login_url='login')
def invoice(request, pk):
    user = models.Users.objects.get(user=request.user.id)
    order = models.Orders.objects.get(order_id=pk)
    item = json.loads(order.items_json)
    datalist = []
    subtotal = 0
    for i in item:
        id = i.split("pr")[1]
        qty = item[i][0]
        product = pmodel.Product.objects.get(id=id)
        price = pmodel.Product.objects.get(id=id).price
        total = int(qty)*int(price)
        datadict = {
            'name' : pmodel.Product.objects.get(id=id).name if pmodel.Product.objects.get(id=id).name else '',
            'category' : pmodel.Product.objects.get(id=id).category if pmodel.Product.objects.get(id=id).category else '',
            'price' : pmodel.Product.objects.get(id=id).price if pmodel.Product.objects.get(id=id).price else '',
            'qty':qty,
            'description':pmodel.Product.objects.get(id=id).description if pmodel.Product.objects.get(id=id).description else '',
            'total': total
        }
        subtotal = subtotal+total

        datalist.append(datadict)
    dict = {'data': datalist,'user':user,'order':order,'subtotal':subtotal}



    return render(request,'invoice.html',context=dict)


@login_required(login_url='adminlogin')
def admin_invoice(request, pk):
    order = models.Orders.objects.get(order_id=pk)
    item = json.loads(order.items_json)
    datalist = []
    subtotal = 0
    for i in item:
        id = i.split("pr")[1]
        qty = item[i][0]
        product = pmodel.Product.objects.get(id=id)
        price = pmodel.Product.objects.get(id=id).price
        total = int(qty)*int(price)
        datadict = {
            'name' : pmodel.Product.objects.get(id=id).name if pmodel.Product.objects.get(id=id).name else '',
            'category' : pmodel.Product.objects.get(id=id).category if pmodel.Product.objects.get(id=id).category else '',
            'price' : pmodel.Product.objects.get(id=id).price if pmodel.Product.objects.get(id=id).price else '',
            'qty':qty,
            'description':pmodel.Product.objects.get(id=id).description if pmodel.Product.objects.get(id=id).description else '',
            'total': total
        }
        subtotal = subtotal+total

        datalist.append(datadict)
    dict = {'data': datalist,'order':order,'subtotal':subtotal}



    return render(request,'invoice.html',context=dict)






def html_render(request):

    return render(request,'test.html')


def single_div(request):

    return render(request,'demodiv.html')