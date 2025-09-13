"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name='index'),
    path('home/',adhome, name='home'),
    path('userlogin/',userlogin, name='userlogin'),
    path('register/',register, name='register'),
    path('cart/',view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/',add_to_cart, name='add_to_cart'),
    path('index/',index, name='index'),
    
    # Admin URLs
    # path('admin-login/', views.admin_login_custom, name='admin_login_custom'),
    # path('admin-logout/', views.admin_logout_custom, name='admin_logout_custom'),
    # path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('admin/products/', views.admin_product_list, name='admin_product_list'),
    # path('admin/products/create/', views.admin_product_create, name='admin_product_create'),
    # path('admin/products/edit/<int:product_id>/', views.admin_product_edit, name='admin_product_edit'),
    # path('admin/products/delete/<int:product_id>/', views.admin_product_delete, name='admin_product_delete'),
    path("", indexx, name="home"),
    path("admin-login/", admin_login, name="admin_login"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("add-product/", add_product, name="add_product"),
    path("edit-product/<int:pk>/", edit_product, name="edit_product"),
    path("delete-product/<int:pk>/", delete_product, name="delete_product"),
]
