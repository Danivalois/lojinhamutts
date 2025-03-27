from django import forms
from orders.models import Freight

class CheckoutForm(forms.Form):
   
    # Customer Information

    customer_name = forms.CharField(max_length=100, required=True, disabled=False)
    customer_phone = forms.CharField(max_length=15, required=True)
    customer_email = forms.EmailField(required=True)
    customer_cpf = forms.CharField(max_length=11, required=True)

    # Address Fields
    customer_zip_code = forms.CharField(
        required=False,  
        max_length=9,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )
    customer_street = forms.CharField(max_length=255, 
        required=False,  
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )
    customer_neighborhood = forms.CharField(max_length=100, 
        required=False,  
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )
    customer_city = forms.CharField(max_length=100, 
        required=False,  
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )
    customer_state = forms.CharField(max_length=2, 
        required=False,  
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
    )
    customer_house_number = forms.CharField(max_length=10, required=True)
    customer_complement = forms.CharField(max_length=100, required=False)

    # Order Fields
    order_quantity = forms.IntegerField(disabled=True)
    order_freight_service=forms.IntegerField(disabled=True)
    order_freight_leadtime=forms.IntegerField(disabled=True)
    order_total_price = forms.DecimalField(disabled=True)
    
    # Freight 
    price_sedex = forms.DecimalField(disabled=True)
    leadtime_sedex = forms.IntegerField(disabled=True)
    total_sedex=forms.DecimalField(disabled=True)
    price_pac = forms.DecimalField(disabled=True)
    leadtime_pac = forms.IntegerField(disabled=True)
    total_pac=forms.DecimalField(disabled=True)
    price_pacmini = forms.DecimalField(disabled=True)
    leadtime_pacmini = forms.IntegerField(disabled=True)
    total_pacmini=forms.DecimalField(disabled=True)
    price_jadlog_exp = forms.DecimalField(disabled=True)
    leadtime_jadlog_exp = forms.IntegerField(disabled=True)
    total_jadlog_exp=forms.DecimalField(disabled=True)
    selected_freight = forms.CharField(widget=forms.RadioSelect(choices=[
        ('PACMINI', 'PACMINI'),
        ('PAC', 'PAC'),
        ('SEDEX', 'SEDEX'),
        ('JADLOG_EXP', 'JADLOG_EXP'),
    ]))

   # Product
    product_code = forms.CharField(
        required=False,  
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),  # ✅ Keeps it visible and included in form submission
    )
    product_short_description = forms.CharField(
    required=False,  
    widget=forms.TextInput(attrs={'readonly': 'readonly'}),  # ✅ Keeps it visible and included in form submission
    )
    product_image_url = forms.CharField(widget=forms.HiddenInput())
    product_unit_price = forms.DecimalField(
        disabled=True,  # Prevent user from editing
        required=False,  # Avoid validation issues
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),  # Extra security

    )

    
class PrecheckoutForm(forms.Form):
    product_code = forms.CharField(widget=forms.HiddenInput())
    product_short_description = forms.CharField(
    required=False,  
    widget=forms.TextInput(attrs={'readonly': 'readonly'}),  # ✅ Keeps it visible and included in form submission
    )
    product_image_url = forms.CharField(widget=forms.HiddenInput())
    product_unit_price = forms.DecimalField(
        disabled=True,  # Prevent user from editing
        required=False,  # Avoid validation issues
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),  # Extra security
    )
    customer_zip_code = forms.CharField(
        max_length=9,
    )
    order_quantity = forms.IntegerField(min_value=1, required=True, initial=1)


    
