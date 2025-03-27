from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from . import forms
from .forms import EditProductForm  # Import the new form



@login_required(login_url="/accounts/login/")
def product_list(request):
    products = Product.objects.all().order_by('product_code')
    return render(request, 'products/product_list.html', {'products': products})

@login_required(login_url="/accounts/login/")
def product_detail(request, product_codeweb):
    product = get_object_or_404(Product, product_code=product_codeweb)
    return render(request, 'products/product_detail.html', { 'products': product })

@login_required(login_url="/accounts/login/")
def product_create(request):
    if request.method == 'POST':
        form = forms.CreateProduct(request.POST, request.FILES) # files é a imagem
        if form.is_valid():
           form.save()
           return redirect('products:product_list')
    else:
        form = forms.CreateProduct()
    return render(request, 'products/product_create.html', { 'form': form })

@login_required(login_url="/accounts/login/")
def product_edit(request, product_code): #Pass product code by url
    product = get_object_or_404(Product, product_code=product_code)  # Look up by product_code
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product) # Bind to existing product
        if form.is_valid():
            form.save() # Save the changes
            return redirect('products:product_list')  # Redirect to product list URL
    else:
        form = EditProductForm(instance=product)  # Populate form with existing product data
    return render(request, 'products/product_edit.html', {'form': form, 'product': product})

@login_required(login_url="/accounts/login/")
def product_delete(request, product_code):
    product = get_object_or_404(Product, product_code=product_code)  # Look up by product_code
    if request.method == 'POST':
        product.delete()
        print("✅ Product Deleted Successfully")
        return redirect('products:product_list')
    print (product_code)
    return render(request, 'products/product_delete.html', {'product': product})

