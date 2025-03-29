from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from . import forms
from .forms import EditProductForm, ProductForm
from supabase import create_client
import os
import mimetypes

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "product-images")
SUPABASE_PATH_PREFIX = os.getenv("SUPABASE_PATH_PREFIX", "products/")

@login_required(login_url="/accounts/login/")
def product_list(request):
    products = Product.objects.all().order_by('product_code')
    return render(request, 'products/product_list.html', {'products': products})

@login_required(login_url="/accounts/login/")
def product_detail(request, product_code):
    product = get_object_or_404(Product, product_code=product_code)
    return render(request, 'products/product_detail.html', { 'products': product })

@login_required(login_url="/accounts/login/")
def product_create(request):
    if request.method == 'POST':
        form = forms.ProductForm(request.POST) # files é a imagem
        if form.is_valid():
            product = form.save(commit=False)
            # Upload new image if provided
            uploaded_file = request.FILES.get("image_upload")
            if uploaded_file:
                product.product_image_url = upload_to_supabase(uploaded_file)
            product.save()
        return redirect('products:product_list')
    else:
        form = forms.ProductForm()
    return render(request, 'products/product_create.html', { 'form': form })

# @login_required(login_url="/accounts/login/")
# def product_edit(request, product_code): #Pass product code by url
#     product = get_object_or_404(Product, product_code=product_code)  # Look up by product_code
#     if request.method == 'POST':
#         form = EditProductForm(request.POST, request.FILES, instance=product) # Bind to existing product
#         if form.is_valid():
#             form.save() # Save the changes
#             return redirect('products:product_list')  # Redirect to product list URL
#     else:
#         form = EditProductForm(instance=product)  # Populate form with existing product data
#     return render(request, 'products/product_edit.html', {'form': form, 'product': product})

@login_required(login_url="/accounts/login/")
def product_delete(request, product_code):
    product = get_object_or_404(Product, product_code=product_code)  # Look up by product_code
    if request.method == 'POST':
        product.delete()
        print("✅ Product Deleted Successfully")
        return redirect('products:product_list')
    print (product_code)
    return render(request, 'products/product_delete.html', {'product': product})

client = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_to_supabase(file):
    filename = file.name
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    file_data = file.read()

    full_path = f"{SUPABASE_PATH_PREFIX}{filename}"

    # Upload the image
    client.storage.from_(SUPABASE_BUCKET).upload(
        path=full_path,
        file=file_data,
        file_options={
            "content-type": content_type,
            "x-upsert": "true"
        }
    )

    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{full_path}"
    return public_url

@login_required(login_url="/accounts/login/")
def product_edit(request, product_code):
    product = get_object_or_404(Product, product_code=product_code)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            product = form.save(commit=False)

            # Upload new image if provided
            uploaded_file = request.FILES.get("image_upload")
            if uploaded_file:
                product.product_image_url = upload_to_supabase(uploaded_file)

            product.save()
            return redirect('products:product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, "products/product_edit.html", {"form": form, "product": product})

