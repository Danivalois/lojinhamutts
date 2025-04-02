from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, Http404
from django.urls import reverse  # Import reverse to generate URLs dynamically
from customers.models import Customer, Address
from products.models import Product
from orders.models import Order, Freight
import uuid  # ✅ For generating order ID
from .forms import CheckoutForm, PrecheckoutForm
from .services import fetch_address_by_zip, fetch_freight_cost, validate_modulo11
from django.conf import settings 
from django.contrib import messages 
import requests
import json
import os
from dotenv import load_dotenv
from django.http import HttpResponseRedirect, HttpResponse
from .services import send_order_emails



MERCADOPAGO_ACCESS_TOKEN = os.getenv("MERCADOPAGO_ACCESS_TOKEN")  # Store in .env file


def precheckout_view(request):
    product_code = request.GET.get('productCode', '').strip()  # ✅ Default to empty string if missing
    if not product_code:  
        raise Http404("Product code is missing")
    product = get_object_or_404(Product, product_code=product_code)  # ✅ Now it won't crash
    form = PrecheckoutForm(initial={
        'product_code': product.product_code,
        'product_short_description': product.product_short_description,
        'product_image_url': product.product_image_url,
        'product_unit_price': product.product_unit_price,        
    })
    return render(request, 'checkouts/precheckout.html', {'form': form})

def custom_404_view(request, exception=None):
    return render(request, "404.html", status=404)


def checkout_view(request):
    if request.method == "POST":
        product_code = request.POST.get('product_code')
        zip_code = request.POST.get('customer_zip_code')
        quantity = request.POST.get('order_quantity')

        # Validate inputs
        
        if not product_code or not zip_code or not quantity:
            return redirect(reverse('checkouts:precheckout') + f"?productCode={product_code}")

        try:
            quantity = int(quantity)
        except ValueError:
            messages.error(request, "Quantidade mínima uma unidade")
            return redirect(reverse('checkouts:precheckout') + f"?productCode={product_code}")
        # Fetch product details
        product = get_object_or_404(Product, product_code=product_code)

        # Fetch address data
        address_data = fetch_address_by_zip(zip_code)
        if not address_data:
            messages.error(request, "CEP Inválido")
            return redirect(reverse('checkouts:precheckout') + f"?productCode={product_code}")

        # Calculate total weight for shipping
        product_wgt = quantity * product.product_weight
        product_cubado=product.product_length + product.product_width + product.product_height
        if product_wgt > 30 or product.product_length>70 or product.product_width>70 or product.product_height>70 or product_cubado>90:
            messages.error(request, "Dimensões do produto ou peso excedendo o limite")
            return redirect(reverse('checkouts:precheckout') + f"?productCode={product_code}")
    
            # Fetch freight costs for all services
        freight_data = fetch_freight_cost(zip_code, product_wgt, product.product_height, product.product_width, product.product_length)


        # Prefill checkout form dynamically
        form_initial_data = {
            'customer_zip_code': zip_code,
            'order_quantity': quantity,
            'customer_street': address_data.get('logradouro', ''),
            'customer_neighborhood': address_data.get('bairro', ''),
            'customer_city': address_data.get('localidade', ''),
            'customer_state': address_data.get('uf', ''),
            'product_code': product.product_code,
            'product_short_description': product.product_short_description,
            'product_image_url': product.product_image_url,
            'product_unit_price': product.product_unit_price,
        }
        
        pu = float(product.product_unit_price)
        qty=float(quantity)
        total_price = (pu * qty)
        # Loop through freight data and populate the form
        for service in ["SEDEX", "PAC", "PACMINI", "JADLOG_EXP"]:
            form_initial_data[f"price_{service.lower()}"] = freight_data.get(service, {}).get("valor", "Unavailable")
            form_initial_data[f"leadtime_{service.lower()}"] = freight_data.get(service, {}).get("prazo", "Unavailable")
            if freight_data.get(service, {}).get("valor", "Unavailable") == "0.00":
              form_initial_data[f"total_{service.lower()}"] = "0.00"
            else:  
              form_initial_data[f"total_{service.lower()}"] = float(freight_data.get(service, {}).get("valor", "Unavailable"))+total_price
        # Calculate total price with PAC as the default shipping option (you can change this)
        form = CheckoutForm(initial=form_initial_data)
        return render(request, 'checkout/checkout.html', {'form': form})

    # If accessed via GET, redirect with productCode in URL
    return redirect(reverse('checkouts:precheckout') + f"?productCode={request.GET.get('productCode', '')}")



def validate_cpf(request):
    if request.method == "POST":
        phone=request.POST.get("customer_phone")
        email=request.POST.get("customer_email")
        house_number=request.POST.get("customer_house_number")
        name=request.POST.get("customer_name")
        #flag_empty=fill_check(phone, email, house_number)
        if phone=='' or email=='' or house_number=='' or name=='':
            flag_empty=False
        else:
            flag_empty=True    
        if "terms_accepted" not in request.POST:
            flag_empty=False
        cpf = request.POST.get("customer_cpf")  # Get CPF from the submitted form
        selected_freight = request.POST.get("selected_freight")
        is_valid = validate_modulo11(cpf)  # Assuming this is your CPF validation logic
        if is_valid and flag_empty:
            form_data = request.POST.copy()  
            # ✅ Instead of redirecting, render a hidden form with the form data
            return render(request, "checkouts/post_redirect.html", {"form_data": form_data})

        else:
          form_data = request.POST.copy()  # Make a mutable copy of POST data
          form_data["selected_freight"] = selected_freight

          
        #recalculating the total price
        pu = request.POST.get("product_unit_price")
        pu = pu.replace(",", ".") 
        qty = float(request.POST.get("order_quantity", "1"))  # Default to 1 to avoid division by zero
        total_price = float(pu) * qty  # Calculate total product price
        # Loop through each shipping option
        for service in ["sedex", "pac", "pacmini", "jadlog_exp"]:
            # Convert price from form (e.g., "10,00" to 10.00)
            freight_price = round(float(request.POST.get(f"price_{service}", "0")), 2)
            # Calculate total including freight
            form_data[f"total_{service}"] = round(freight_price + total_price, 2)
           
        
        product_code = form_data["product_code"]
        product = get_object_or_404(Product, product_code=product_code)
        form_data["product_image_url"] = product.product_image_url or ""
        form = CheckoutForm(initial=form_data)
        if is_valid == False and flag_empty == False:
            message="Todos os campos são obrigatórios.  CPF Inválido."
        else:       
            if flag_empty == False:
                message="Todos os campos são obrigatórios."
            else:
                form_data["customer_cpf"] = ""  # Clear CPF field
                message="CPF inválido."
        messages.error(request, message)
        return render(request, "checkout/checkout.html", {
            "form": form,  # Send updated form instance
            "error": "CPF inválido! Corrija antes de continuar."
            })




def process_payment(request):
    if request.method == "POST":
        try:
            # ✅ Retrieve form data
            product_code = request.POST.get("product_code")
            product_description = request.POST.get("product_short_description")
            product_image_url = request.POST.get("product_image_url")
            unit_price = round(float(request.POST.get("product_unit_price", "0").replace(",", ".")), 2)
            quantity = int(request.POST.get("order_quantity"))

            # ✅ Get selected freight
            freight_service_name = request.POST.get("selected_freight", "").upper()
            shipping_cost = round(float(request.POST.get(f"price_{freight_service_name.lower()}", 0)), 2)
            leadtime = int(request.POST.get(f"leadtime_{freight_service_name.lower()}", 0))

            # ✅ Customer Details
            customer_email = request.POST.get("customer_email")
            customer_name = request.POST.get("customer_name")
            customer_cpf = request.POST.get("customer_cpf")
            zip_code = request.POST.get("customer_zip_code")
            street = request.POST.get("customer_street")
            neighborhood = request.POST.get("customer_neighborhood")
            city = request.POST.get("customer_city")
            state = request.POST.get("customer_state")
            house_number = request.POST.get("customer_house_number")
            complement = request.POST.get("customer_complement")
            phone = request.POST.get("customer_phone")
            customer_name = request.POST.get("customer_name", "").strip()
            if not customer_name:
                return JsonResponse({"error": "Customer name is required."}, status=400)

            # ✅ Step 1: Create or Get Customer
            customer, created = Customer.objects.get_or_create(
                customer_cpf=customer_cpf,
                defaults={"customer_name": customer_name}
            )

            if not created and customer_name:  # Update only if customer_name is provided
                customer.customer_name = customer_name  
                customer.save()

            # ✅ Step 2: Create or Get Address
            address, created = Address.objects.get_or_create(
                customer=customer,
                customer_zip_code=zip_code,
                defaults={
                    "customer_street": street,
                    "customer_neighborhood": neighborhood,
                    "customer_city": city,
                    "customer_state": state,
                    "customer_house_number": house_number,
                    "customer_complement": complement,
                    "customer_phone": phone,
                    "customer_email": customer_email,
                }
            )
            if not created:
                # Update existing address if needed
                address.customer_street = street
                address.customer_neighborhood = neighborhood
                address.customer_city = city
                address.customer_state = state
                address.customer_house_number = house_number
                address.customer_complement = complement
                address.customer_phone = phone
                address.customer_email = customer_email
                address.save()

            # ✅ Step 3: Get Freight Service
            freight_service, _ = Freight.objects.get_or_create(freight_service=freight_service_name)

            # ✅ Step 4: Create Order Entry
            order_id = str(uuid.uuid4())  # Generate unique order ID
            order = Order.objects.create(
                order_customer=customer,
                order_product=get_object_or_404(Product, product_code=product_code),
                order_address=address,
                order_ID=order_id,
                order_payment_ID="",  # Set after Mercado Pago response
                order_status="pending_payment",
                order_quantity=quantity,
                order_freight_cost=shipping_cost,
                product_unit_price=unit_price,
                order_freight_service=freight_service,
                order_leadtime=leadtime,
                order_is_active=True
            )

            # ✅ Step 5: Create Mercado Pago Order Data
            order_data = {
                "items": [{
                    "title": product_description,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "currency_id": "BRL",
                    "picture_url": f"{request.scheme}://{request.get_host()}{product_image_url}",
                }],
                "shipments": {
                    "cost": shipping_cost,
                    "mode": "not_specified",
                },
                "payer": {"email": customer_email},
                "back_urls": {
                    "success": f"{request.scheme}://{request.get_host()}/checkouts/payment-success/?order_id={order_id}",
                    "failure": f"{request.scheme}://{request.get_host()}/checkouts/payment-failure/",
                    "pending": f"{request.scheme}://{request.get_host()}/checkouts/payment-pending/",
                },

                
                "auto_return": "approved",
            }

            # ✅ Send Request to Mercado Pago API
            MERCADOPAGO_API_URL = "https://api.mercadopago.com/checkout/preferences"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {MERCADOPAGO_ACCESS_TOKEN}"
            }
            response = requests.post(MERCADOPAGO_API_URL, headers=headers, data=json.dumps(order_data))

            if response.status_code == 201:
                response_data = response.json()
                order.order_payment_ID = response_data["id"]
                order.save()

                # ✅ Redirect user to Mercado Pago checkout URL
                return HttpResponseRedirect(response_data["init_point"])

            else:
                print("❌ Mercado Pago API Error:", response.text)
                return JsonResponse({"error": "Failed to create payment preference", "details": response.text}, status=500)

        except Exception as e:
            print(f"❌ Error processing payment: {str(e)}")
            return JsonResponse({"error": "Failed to process payment", "details": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)




def payment_success(request):
    # Extract parameters from Mercado Pago's GET request
    collection_id = request.GET.get("collection_id")  # Mercado Pago order ID
    payment_id = request.GET.get("payment_id")  # Payment transaction ID
    payment_status = request.GET.get("status")  # Payment status
    payment_type = request.GET.get("payment_type")  # Payment method (credit_card, account_money, etc.)
    site_id = request.GET.get("site_id")  # Mercado Pago site (e.g., "MLB" for Brazil)
    order_id = request.GET.get("order_id")  # Our internal order ID (sent in URL)

    # Ensure we have all required data
    if not order_id or not collection_id or not payment_id or not payment_status:
        return HttpResponse("❌ Erro: Parâmetros inválidos na resposta do Mercado Pago.", status=400)

    # ✅ Step 1: Retrieve the Order from Database
    order = get_object_or_404(Order, order_ID=order_id)

    # ✅ Step 2: Update the Order's Payment Information
    order.order_ID = order_id  # Update with Mercado Pago's collection_id
    order.order_payment_ID = payment_id  # Update payment transaction ID
    order.order_status = payment_status  # Update status (approved, pending, etc.)
    order.order_pmt_type = payment_type  # Update payment method (credit_card, boleto, etc.)
    order.order_site_id = site_id  # Update site ID (MLB, etc.)
    order.save()  # ✅ Save changes to database

    # ✅ Step 3: Display Confirmation Message
    message = "✅ Pagamento confirmado! Seu pedido foi atualizado."
    if payment_status == "pending":
        message = "⏳ Pagamento pendente. Aguarde a confirmação."
    elif payment_status in ["rejected", "cancelled"]:
        message = "❌ O pagamento foi recusado ou cancelado."
        
    send_order_emails(order)

    return render(request, "checkouts/payment_success.html", {
        "message": message,
        "order_id": order_id,
        "payment_id": payment_id,
        "status": payment_status,
        "payment_type": payment_type,
        "site_id": site_id
    })

def payment_failure(request):
    return render(request, "checkouts/payment_failure.html", {"message": "O pagamento falhou. Tente novamente."})

def payment_pending(request):
    return render(request, "checkouts/payment_pending.html", {"message": "Seu pagamento está pendente. Aguarde a confirmação."})

def terms_use_view(request):
    return render(request, 'checkouts/terms_use.html')
