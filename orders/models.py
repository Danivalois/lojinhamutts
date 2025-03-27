from django.db import models
from django.core.exceptions import ValidationError


class Freight(models.Model):
    freight_service = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.freight_service


class Order(models.Model):
    order_customer = models.ForeignKey("customers.Customer", on_delete=models.SET_NULL, null=True)
    order_product = models.ForeignKey("products.Product", on_delete=models.SET_NULL, null=True)
    order_address = models.ForeignKey("customers.Address", on_delete=models.SET_NULL, null=True)
    order_ID = models.CharField(max_length=100, unique=True)
    order_payment_ID = models.CharField(max_length=100, unique=True, blank=True, null=True)
    order_status = models.CharField(max_length=50)
    order_pmt_type=models.CharField(max_length=50, null=True)
    order_site_id=models.CharField(max_length=50, null=True)
    order_quantity = models.IntegerField()
    order_freight_cost = models.DecimalField(max_digits=10, decimal_places=2, default='0.01')
    product_unit_price = models.DecimalField(max_digits=10, decimal_places=2, default='0.01')
    order_freight_service = models.ForeignKey(Freight, on_delete=models.SET_NULL, null=True)
    order_leadtime=models.IntegerField(null=True)
    order_created_at = models.DateTimeField(auto_now_add=True)
    order_updated_at = models.DateTimeField(auto_now=True)
    order_is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Order {self.order_ID}"