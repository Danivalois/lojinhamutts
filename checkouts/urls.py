from django.urls import path
from . import views
from .views import terms_use_view  

app_name = 'checkouts'

urlpatterns = [
    path('', views.precheckout_view, name='precheckout'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('validate-cpf/', views.validate_cpf, name='validate_cpf'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failure/', views.payment_failure, name='payment_failure'),
    path('payment-pending/', views.payment_pending, name='payment_pending'),
    path('terms-use/', terms_use_view, name='terms_use'),
   
]

