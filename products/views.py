from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from . import forms
from .forms import EditProductForm, ProductForm
from supabase import create_client
import os
import mimetypes
import boto3
from django.conf import settings
import mimetypes



SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "product-images")
SUPABASE_PATH_PREFIX = os.getenv("SUPABASE_PATH_PREFIX", "products/")


def upload_to_cloudflare(file):
    
    bucket_name = os.environ.get('CLOUDFLARE_BUCKET_NAME')
    original_filename = file.name
    filename = clean_filename(original_filename) # Using your existing clean function
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    # 1. Initialize the S3 client to point to Cloudflare
    s3_client = boto3.client(
        's3',
        endpoint_url=settings.CLOUDFLARE_R2_ENDPOINT,
        aws_access_key_id=settings.CLOUDFLARE_ACCESS_KEY,
        aws_secret_access_key=settings.CLOUDFLARE_SECRET_KEY,
        region_name='auto'  # R2 ignores this, but boto3 requires it
    )

    full_path = f"products/{filename}"
    print("XXXX uploading to R2 path:", full_path)

    # 2. Upload the file to the bucket




    s3_client.upload_fileobj(
        file,
        bucket_name,
        full_path,
        ExtraArgs={
            'ContentType': content_type,
            # We don't need 'x-upsert' here; boto3 overwrites files with the same name by default
        }
    )

    # 3. Construct and return the public URL so the view can save it to the database
    public_url = f"{settings.CLOUDFLARE_PUBLIC_DOMAIN}/{full_path}"
    print("XXXX new public url:", public_url)
    
    return public_url



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
                product.product_image_url = upload_to_cloudflare(uploaded_file)
            product.save()
        return redirect('products:product_list')
    else:
        form = forms.ProductForm()
    return render(request, 'products/product_create.html', { 'form': form })

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


from django.utils.text import slugify
import os

def clean_filename(filename):
    name, ext = os.path.splitext(filename)
    clean_name = slugify(name)  # removes accents + spaces
    return f"{clean_name}{ext.lower()}"


def upload_to_supabase(file):
    filename = file.name
    original_filename = file.name
    filename = clean_filename(original_filename)


    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    file_data = file.read()

    full_path = f"{SUPABASE_PATH_PREFIX}{filename}"
    print("XXXX full_path", full_path)
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
    print("XXXX public url", public_url)
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
                product.product_image_url = upload_to_cloudflare(uploaded_file)

            product.save()
            return redirect('products:product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, "products/product_edit.html", {"form": form, "product": product})

