from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from customers.models import Customer, Address
from products.models import Product
from orders.models import Order, Freight
from django.contrib.auth.decorators import login_required
from . import forms
from .forms import CreateOrder




@login_required(login_url="/accounts/login/")
def order_delete(request, order_ID):
    order = get_object_or_404(Order, order_ID=order_ID)
    if request.method == 'POST':
        order.delete()
        print("✅ Order Deleted Successfully")
        return redirect('orders:order_list')
    return render(request, 'orders/order_delete.html', {'order': order})

@login_required(login_url="/accounts/login/")
def order_list(request):
    orders = Order.objects.all().order_by('order_created_at')
    for order in orders:
        try:
            order.order_total_price = (
                order.order_quantity * order.product_unit_price
            ) + order.order_freight_cost
        except Exception as e:
            order.order_total_price = "Erro: " + str(e)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required(login_url="/accounts/login/")
def order_show(request, order_ID):
    order = get_object_or_404(Order, order_ID=order_ID)
    if request.method == 'POST':
        form = forms.CreateOrder(request.POST, instance=order)
        if form.is_valid():
            form.save() 
        return redirect('orders:order_list') 
    else:
        form = forms.CreateOrder(instance=order)
    order_total_price = (order.order_quantity * order.product_unit_price) + order.order_freight_cost    
    return render(request, 'orders/order_show.html', {'form': form, 'order': order, 'order_total_price':order_total_price,})
