import requests
import re
from dotenv import load_dotenv
from decimal import Decimal
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from orders.models import Order

load_dotenv()  # Load environment variables from .env file

def fetch_address_by_zip(zip_code):
    """Fetches address details from an external API like ViaCEP."""
    url = f"https://viacep.com.br/ws/{zip_code}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "erro" in data:  # ViaCEP returns "erro" for invalid ZIP codes
            return None
        return data
    
    return None  # Handle cases where API is down or request fails



def validate_modulo11(value):
    """Validate CPF using Modulo 11 algorithm."""
    cpf = re.sub(r'\D', '', value)  # Remove all non-numeric characters

    # CPF must have exactly 11 digits
    if len(cpf) != 11:
        return False

    # Check if all digits are the same (invalid CPF)
    if cpf == cpf[0] * 11:
        return False

    # Validate first digit
    sum_first = sum(int(cpf[i]) * (10 - i) for i in range(9))
    first_digit = (sum_first * 10 % 11) % 10

    # Validate second digit
    sum_second = sum(int(cpf[i]) * (11 - i) for i in range(10))
    second_digit = (sum_second * 10 % 11) % 10

    return int(cpf[9]) == first_digit and int(cpf[10]) == second_digit  # Return True if valid



def clean_number(value):
    """Formats numbers with two decimal places and converts them to a string."""
    value = float(value) if isinstance(value, Decimal) else value  # Ensure it's a float
    return f"{value:.2f}"  # Format as string with 2 decimal places

import requests
import os
from decimal import Decimal

def clean_number(value):
    """Formats numbers with two decimal places and converts them to a string."""
    value = float(value) if isinstance(value, Decimal) else value  # Ensure it's a float
    return f"{value:.2f}"  # Format as string with 2 decimal places

def fetch_freight_cost(customer_zip_code, product_weight, product_height, product_width, product_length):
    # Define the freight services to check
    freight_services = ["SEDEX", "PAC", "MINIPAC", "JADLOG_EXP"]
    
    freight_results = {}

    for service in freight_services:
        # Prepare the payload as form-data (key-value pairs)
        payload = {
            "plataforma_id": "66780",
            "plataforma_chave": "$2y$10$1uqdW6t3fFS.4nk7nueRDujOYSPvTf81RSF88NADpFQXTjmT5C.HS",
            "cep_origem": "22793084",
            "cep_destino": customer_zip_code.replace("-", ""),  # Remove dash from ZIP
            "valor_seguro": "",  # Optional, add if required
            "servico": service,
            "peso": clean_number(product_weight),
            "altura": clean_number(product_height),
            "largura": clean_number(product_width),
            "comprimento": clean_number(product_length),
 
        }

        try:
            # Send the request as form-data (not JSON)
            response = requests.post("https://mandabem.com.br/ws/valor_envio", data=payload, timeout=10)  
            #print(f'Manda Bem response for {service}:', response.status_code, response.text)

            if response.status_code == 200:
                data = response.json()
                if "resultado" in data and service in data["resultado"]:
                    freight_results[service] = {
                        "valor": data["resultado"][service].get("valor", "0.00"),
                        "prazo": data["resultado"][service].get("prazo", ""),
                    }
                else:
                    print(f"Warning: No valid response for {service}")
                    freight_results[service] = {"valor": "0.00", "prazo": ""}
            else:
                #print(f"API request failed for {service} with status {response.status_code}")
                freight_results[service] = {"valor": "0.00", "prazo": ""}
        except requests.RequestException as e:
            #print(f"Request failed for {service}: {e}")
            freight_results[service] = {"valor": "0.00", "prazo": ""}

    return freight_results  # Returns a dictionary with all freight options




def send_order_emails(order):
    """
    Sends an email to both the Admin and Customer after a successful payment.
    """
    try:
        total_order_amount = (order.product_unit_price * order.order_quantity) + order.order_freight_cost
        # ✅ Construct the Absolute Product Image URL
        product_image_url = (
            f"{settings.SITE_URL}{order.order_product.product_image_url.url}"
            if order.order_product.product_image_url
            else ""
        )        
        

        
        # ✅ Admin Email
        admin_subject = f"📦 New Order Received - {order.order_ID}"
        admin_message = render_to_string("emails/admin_order_email.html", {
            "order": order,
            "total_order_amount": total_order_amount,  # Pass computed value
            "product_image_url": product_image_url  # Pass Image URL
        })
        send_mail(
            subject=admin_subject,
            message="teste admin",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["apln2911@gmail.com"],  # Change to your admin email
            html_message=admin_message,
            fail_silently=False,
        )

# ✅ Customer Email
        customer_subject = f"🎉 Order Confirmation - {order.order_ID}"
        customer_message = render_to_string("emails/customer_order_email.html", {
            "order": order,
            "total_order_amount": total_order_amount,  # Pass computed value
            "product_image_url": product_image_url  # Pass Image URL
        })
        send_mail(
            subject=customer_subject,
            message="teste customer",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.order_address.customer_email],
            html_message=customer_message,
            fail_silently=False,
        )

        print(f"✅ Order emails sent successfully for Order {order.order_ID}")

    except Exception as e:
        print(f"❌ Failed to send order emails: {str(e)}")





