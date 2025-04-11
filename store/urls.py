"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import (
    product_list, product_detail, product_create,
    product_update, product_delete, register,
    user_login, user_logout, verify, logout_view
)
from . import views, api_views

router = DefaultRouter()
router.register(r'products', api_views.ProductViewSet)
router.register(r'categories', api_views.CategoryViewSet)



urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('product/create/', product_create, name='product_create'),
    path('product/update/<int:pk>/', product_update, name='product_update'),
    path('product/delete/<int:pk>/', product_delete, name='product_delete'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('verify/', verify, name='verify'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('api/login/', api_views.Login.as_view(), name='api-login'),
    path('api/', include((router.urls, 'api'), namespace='api')),
]