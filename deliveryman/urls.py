from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
               path('register/', views.dman_registration, name='dman_registration'),
               path('login/', LoginView.as_view(template_name='delivery/login.html'), name='dman_login'),
               path('dashboard/', views.dashboard, name='dman_dashboard'),
               path('product-details/', views.product_details, name='vendor_dashboard'),
               path('product-edit/<int:pk>', views.edit, name='edit'),
               path('order-details', views.product_orders, name='edit'),

]
