from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Address
from django.contrib.auth.decorators import login_required
from . import forms


@login_required(login_url="/accounts/login/")
def customer_create(request):
    if request.method == 'POST':
        customer_form = forms.CreateCustomerForm(request.POST)
        address_form = forms.CreateAddressForm(request.POST)

        if customer_form.is_valid() and address_form.is_valid():
            customer = customer_form.save()
            address = address_form.save(commit=False)
            address.customer = customer
            address.save()
            return redirect('customers:customer_list')
       
    else:
        customer_form = forms.CreateCustomerForm(initial={'customer_cpf': ''})
        address_form = forms.CreateAddressForm()

    return render(request, 'customers/customer_create.html', {
        'customer_form': customer_form,
        'address_form': address_form,
    })

@login_required(login_url="/accounts/login/")
def customer_list(request):
    customers = Customer.objects.all()
    addresses = Address.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers, 'addresses': addresses})


@login_required(login_url="/accounts/login/")
def customer_list_cpf(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list_cpf.html', {'customer': customers})


@login_required(login_url="/accounts/login/")
def customer_list_address(request):
    addresses = Address.objects.select_related('customer').all().order_by('customer_zip_code')  # Optimized query
    return render(request, 'customers/customer_list_address.html', {'addresses': addresses})

@login_required(login_url="/accounts/login/")
def customer_edit(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.method == 'POST':
        address=forms.CreateAddressForm(request.POST, instance=address)
        #print('address do post', address.customer_complement)
        address.save()
        return redirect('customers:customer_list_address')
    else:
        print('else address', address)
    address_form = forms.CreateAddressForm(instance=address)
    return render(request, 'customers/customer_edit.html', {
        'address_form': address_form,
        'address': address,
    
    })


@login_required(login_url="/accounts/login/")
def customer_delete(request, customer_cpf):
    customer = get_object_or_404(Customer, customer_cpf=customer_cpf)  # Look up by customer_cpf
    if request.method == 'POST':
        customer.delete()
        print("✅ Customer Deleted Successfully")
        return redirect('customers:customer_list')
    print (customer_cpf)
    return render(request, 'customers/customer_delete.html', {'customer': customer})


@login_required(login_url="/accounts/login/")
def customer_delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    print('antes do if POST - address', address)
    if request.method == 'POST':
        address.delete()  # Delete the address fetched using address_id
        print("✅ Address Deleted Successfully")
        return redirect('customers:customer_list_address')
    print ('antes do render', address)
    return render(request, 'customers/customer_delete_address.html', {'address': address})