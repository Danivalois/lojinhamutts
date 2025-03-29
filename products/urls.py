from django.urls import path, re_path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'), #no name collision
    path('create/', views.product_create, name='product_create'), #no name collision
    path('edit/<str:product_code>/', views.product_edit, name='product_edit'),
    path('delete/<str:product_code>/', views.product_delete, name='product_delete'),
    re_path(r'.*?productCode=(?P<product_code>[A-Za-z0-9]+)', views.product_detail, name='product_detail'),
]
