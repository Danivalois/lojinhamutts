from django.urls import path, re_path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'), #no name collision
    #path('create/', views.customer_create, name='customer_create'), #no name collision
    #path('edit/<str:customer_cpf>/', views.customer_edit, name='customer_edit'),
    path('delete/<str:order_ID>/', views.order_delete, name='order_delete'),
    path('showorder/<str:order_ID>/', views.order_show, name='order_show'),
    
]