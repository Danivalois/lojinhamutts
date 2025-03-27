from django.db import models
import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

def validate_cpf(value):
    """Validate CPF using Modulo 11 algorithm."""
    cpf = re.sub(r'\D', '', value)  # Remove all non-numeric characters

    # CPF must have exactly 11 digits
    if len(cpf) != 11:
        raise ValidationError("CPF must contain exactly 11 digits.")

    # Check if all digits are the same (invalid CPF)
    if cpf == cpf[0] * 11:
        raise ValidationError("Invalid CPF: All digits are the same.")

    # Validate first digit
    sum_first = sum(int(cpf[i]) * (10 - i) for i in range(9))
    first_digit = (sum_first * 10 % 11) % 10

    # Validate second digit
    sum_second = sum(int(cpf[i]) * (11 - i) for i in range(10))
    second_digit = (sum_second * 10 % 11) % 10

    if int(cpf[9]) != first_digit or int(cpf[10]) != second_digit:
        raise ValidationError("Invalid CPF: Check digits do not match.")

    return cpf  # Return cleaned CPF


class Customer(models.Model):
    customer_cpf = models.CharField(
        max_length=11, 
        unique=True, 
        validators=[validate_cpf], 
        verbose_name="CPF"
    )
    customer_name = models.CharField(max_length=100, blank=False)
    customer_created_at = models.DateTimeField(auto_now_add=True)
    customer_updated_at = models.DateTimeField(auto_now=True)
    customer_is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.customer_name} ({self.customer_cpf})"


def validate_zip_code(value):
    """Accept both `99999999` and `99999-999` formats."""
    cleaned_value = re.sub(r'[^0-9]', '', value)  # Remove non-numeric characters
    if len(cleaned_value) != 8:
        raise ValidationError("CEP must have 8 digits.")
    return cleaned_value

class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses', null=True, blank=True)
    customer_zip_code = models.CharField(
        max_length=9,
        validators=[validate_zip_code], 
        verbose_name="CEP"
    )
    customer_street = models.CharField(max_length=255, blank=False)
    customer_neighborhood = models.CharField(max_length=100, blank=False)
    customer_city = models.CharField(max_length=100, blank=False)
    customer_state = models.CharField(max_length=2, blank=False)  # Ex: SP, RJ
    customer_house_number = models.CharField(max_length=10, blank=False)
    customer_complement = models.CharField(max_length=100, blank=True, null=True)
    customer_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefone")
    customer_email = models.EmailField(blank=True, null=True, validators=[EmailValidator()])

    def __str__(self):
        return f"{self.customer_street}, {self.customer_house_number} - {self.customer_city}/{self.customer_state}"

