from django.shortcuts import render
from . import models


# Create your views here.

def index(request):
    return render(request, 'index.html')


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


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_vendor(user):
    return user.groups.filter(name='VENDOR').exists()



def afterlogin_view(request):
    if is_vendor(request.user):
        return redirect('vendor/dashboard')

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
    #             return render(request, 'teacher/teacher_wait_for_approval.html')
    # else:
    #     return redirect('admin-dashboard')