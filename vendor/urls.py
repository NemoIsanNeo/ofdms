from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
               path('register/', views.vendor_register, name='vendor_register'),
               path('login/', LoginView.as_view(template_name='vendor/login.html'), name='vendor_login'),
               path('dashboard/', views.dashboard, name='vendor_dashboard'),
               path('product-details/', views.product_details, name='vendor_dashboard'),
               path('order-details/', views.product_orders, name='product_orders'),
               path('product-edit/<int:pk>', views.edit, name='edit'),


]
