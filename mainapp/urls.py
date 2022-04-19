from django.urls import path
from . import views
from vendor import views as vviews
from django.contrib.auth.views import LogoutView, LoginView


urlpatterns = [path('', views.index, name='index'),path('index', views.index, name='index'),
               path('login/', LoginView.as_view(template_name='login.html'), name='login'),
               path('register/', views.register, name='register'),
               path('account/', views.account, name='account'),
               path('index/', views.index, name='index'),
               path('order/', views.order, name='order'),
               path('cart_details', views.cart_details, name='cart_details'),
               path('checkout/', views.checkout, name='checkout'),
               path('food_details/', views.food_details, name='food_details'),
               path('food_list/', views.food_list, name='food_list'),
               path('after_login', views.afterlogin_view, name='after_login'),
               path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
               path('sadmin/product-details/', views.product_details, name='product-details'),
               path('sadmin/product-orders/', views.product_orders, name='product-details'),
               path('sadmin/product-category/', views.cat_details, name='product-details'),
               path('sadmin/dman/', views.dman_details, name='dman-details'),
               path('product-category/delete/<int:pk>', views.delete_product_category, name='product-delete'),

               path('sadmin/vendor/', views.vendor, name='product-details'),
               path('product/accept/<int:pk>', views.accept_product, name='product-accept'),
               path('product/reject/<int:pk>', views.reject_product, name='product-reject'),
               path('product/delete/<int:pk>', views.delete_product, name='product-delete'),

               path('vendor/accept/<int:pk>', views.accept_vendor, name='vendor-accept'),
               path('vendor/reject/<int:pk>', views.reject_vendor, name='product-reject'),
               path('vendor/delete/<int:pk>', views.delete_vendor, name='product-delete'),

                path('dman/accept/<int:pk>', views.accept_dman, name='dman-accept'),
               path('dman/reject/<int:pk>', views.reject_dman, name='dman-reject'),
               path('dman/delete/<int:pk>', views.delete_dman, name='dman-delete'),
               path('invoice/<int:pk>', views.invoice, name='product-delete'),
               path('sadmin/invoice/<int:pk>', views.admin_invoice, name='admin-invoice'),

               ]
