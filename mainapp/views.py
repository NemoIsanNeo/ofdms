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
        else:
            print('Nothing')
    return render(request, 'register.html')


def account(request):
    return render(request, 'account.html')


def cart_details(request):
    return render(request, 'cart_details.html')


def checkout(request):
    return render(request, 'checkout.html')
