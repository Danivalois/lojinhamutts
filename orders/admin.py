from django.contrib import admin
from .models import Order
from .models import Freight
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):
    list_display = ('order_ID', 'order_customer', 'order_product', 'order_status', 'order_created_at')
    pass


#admin.site.register(Order)
admin.site.register(Freight)
