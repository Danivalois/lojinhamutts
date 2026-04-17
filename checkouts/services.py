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



def fetch_freight_cost(customer_zip_code, product_weight, product_height, product_width, product_length, quantity=1):
    # Define the API freight services to check
    freight_services = ["SEDEX", "PAC", "PACMINI", "JADLOG_EXP"]
    freight_results = {}

    for service in freight_services:
        payload = {
            "plataforma_id": "66780",
            "plataforma_chave": "$2y$10$1uqdW6t3fFS.4nk7nueRDujOYSPvTf81RSF88NADpFQXTjmT5C.HS",
            "cep_origem": "22793084",
            "cep_destino": customer_zip_code.replace("-", ""),
            "valor_seguro": "",
            "servico": service,
            "peso": clean_number(product_weight),
            "altura": clean_number(product_height),
            "largura": clean_number(product_width),
            "comprimento": clean_number(product_length),
        }
       
        try:
            response = requests.post("https://mandabem.com.br/ws/valor_envio", data=payload, timeout=10)  
            if response.status_code == 200:
                data = response.json()
                if "resultado" in data and service in data["resultado"]:
                    freight_results[service] = {
                        "valor": data["resultado"][service].get("valor", "0.00"),
                        "prazo": data["resultado"][service].get("prazo", ""),
                    }
                else:
                    freight_results[service] = {"valor": "0.00", "prazo": ""}
            else:
                freight_results[service] = {"valor": "0.00", "prazo": ""}
        except requests.RequestException:
            freight_results[service] = {"valor": "0.00", "prazo": ""}

    # --- ADD LOGGI CUSTOM LOGIC HERE ---
    clean_zip = customer_zip_code.replace("-", "")
    if len(clean_zip) >= 2:
        zip_prefix = clean_zip[:2]
        # Check if region is Centro (20), Zona Sul (22), or Zona Oeste (23) AND max 5 units
        if zip_prefix in ['20', '22', '23'] and int(quantity) <= 5:
            freight_results["LOGGI"] = {
                "valor": "12.90",
                "prazo": "4"
            }

    return freight_results



from twilio.rest import Client
from customers.models import Address

def send_whatsapp(order):

    client = Client(
        os.environ.get("TWILIO_ACCOUNT_SID"),
        os.environ.get("TWILIO_AUTH_TOKEN")
    )

    address = order.order_address

    total = (order.product_unit_price * order.order_quantity) + order.order_freight_cost

    message = (
    f"📦 Novo Pedido Recebido\n"
    f"Pedido: {order.order_ID}\n"
    f"Produto: {order.order_product}\n"
    f"CEP: {address.customer_zip_code}\n"
    f"Bairro: {address.customer_neighborhood}\n"
    f"Cidade-UF: {address.customer_city}-{address.customer_state}\n"
    f"Total: R$ {total}"
)

    phones = [
        "whatsapp:+5521996368806",
        "whatsapp:+5521979234334",
   
    ]

    for phone in phones:
        msg = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message,
            to=phone
        )

        print("Sent to:", phone, "SID:", msg.sid)

import requests
import urllib.parse

def send_whatsapp_simple(order, total_amount):
    cb_key = os.environ.get("CHATBOTKEY")
    admin_phone ="5521996368806" # e.g., "+5521999999999"
   
    
    message = f"📦 *Novo Pedido:* {order.order_ID} | Valor: R$ {total_amount:.2f} | Status: {order.order_status}"
    encoded_message = urllib.parse.quote(message)
    
    url = f"https://api.callmebot.com/whatsapp.php?phone={admin_phone}&text={encoded_message}&apikey={cb_key}"

    try:
        requests.get(url)
        print("✅ Simple WhatsApp alert sent.")
    except Exception as e:
        print(f"❌ Simple WhatsApp alert failed: {e}")

def send_order_emails(order):
    """
    Sends an email to both the Admin and Customer after a successful payment.
    """
    print("XXXX order - arrived send email", order)
    try:
        total_order_amount = (order.product_unit_price * order.order_quantity) + order.order_freight_cost
        # ✅ Construct the Absolute Product Image URL
        product_image_url = f"{settings.MEDIA_URL}{order.order_product.product_image_url}" if order.order_product.product_image_url else ""        
        # ✅ Admin Email
        admin_subject = f"📦 Novo Pedido Recebido - {order.order_ID}"
        admin_message = render_to_string("emails/admin_order_email.html", {
            "order": order,
            "total_order_amount": total_order_amount,  # Pass computed value
            "product_image_url": product_image_url  # Pass Image URL
        })
        print("XXXX call send whatsapp")
        send_whatsapp_simple(order, total_order_amount)
        send_mail(
            subject=admin_subject,
            message="teste admin",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["valois.daniela@gmail.com"],  # Change to your admin email
            html_message=admin_message,
            fail_silently=False,
        )


# ✅ Customer Email
        customer_subject = f"🎉 Confirmação de Pedido - {order.order_ID}"
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





