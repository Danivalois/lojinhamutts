from django.urls import path, re_path
from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.customer_list, name='customer_list'), 
    path('customerlistaddress/', views.customer_list_address, name='customer_list_address'),
    path('create/', views.customer_create, name='customer_create'), 
    path('edit/<int:address_id>/', views.customer_edit, name='customer_edit'),
    path('delete/<str:customer_cpf>/', views.customer_delete, name='customer_delete'),
    path('deleteaddress/<int:address_id>/', views.customer_delete_address, name='customer_delete_address'),
]

