from django import forms
from . import models
from django.core.exceptions import ValidationError

class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = [
            'customer_cpf',
            'customer_name',
            'customer_is_active',
        ]
        labels = {
            'customer_cpf': 'CPF:',
            'customer_name': 'Nome Completo:',
            'customer_is_active': 'Cliente está ativo?   ',
        }

class CreateAddressForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = [
            'customer_zip_code',
            'customer_street',
            'customer_neighborhood',
            'customer_city',
            'customer_state',
            'customer_house_number',
            'customer_complement',
            'customer_phone',
            'customer_email',
        ]
    
   

        labels = {
            'customer_zip_code': 'CEP:',
            'customer_street': 'Rua/Av./etc.:',
            'customer_neighborhood': 'Bairro:',
            'customer_city': 'Cidade:',
            'customer_state': 'Estado:',
            'customer_house_number': 'Número:',
            'customer_complement': 'Complemento:',
            'customer_phone': 'Celular:',
            'customer_email': 'E-mail:',
        }
        
