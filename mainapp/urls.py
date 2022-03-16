from django.urls import path
from . import views

urlpatterns = [path('', views.index, name='index'),
               path('login/', views.login, name='login'),
               path('register/', views.register, name='register'),
               path('account/', views.account, name='account'),
               path('cart_details', views.cart_details, name='cart_details'),
               path('checkout/', views.checkout, name='checkout')]
