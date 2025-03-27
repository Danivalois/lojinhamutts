from django import forms
from . import models
from django.core.exceptions import ValidationError

class CreateOrder(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = [
                'order_ID',
                'order_payment_ID',
                'order_status',
                'order_customer',
                'order_address',
                'order_product',
                'order_quantity',
                'product_unit_price',
                'order_freight_service',        
                'order_freight_cost',
                'order_leadtime',
                'order_is_active',
                

        ]
        labels = {
                'order_ID': 'Número da Ordem',
                'order_payment_ID': 'ID do Pagamento',
                'order_status': 'Status da Ordem',
                'order_customer': 'Nome/CPF do Cliente',
                'order_address': 'Endereço do Cliente',
                'order_product': 'Descrição do Produto',
                'order_quantity': 'Quantidade',
                'product_unit_price': 'Preço Unitário',
                'order_freight_service': 'Serviço do Frete',
                'order_freight_cost': 'Valor do Frete',
                'order_leadtime': 'Prazo de Entrega',
                'order_is_active': 'Ordem está ativa?',
                }

