from django.contrib import admin
from .models import Customer, Address
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(Address)
class AddressAdmin(ImportExportModelAdmin):
    list_display = ('customer_zip_code', 'customer_street', 'customer_city')
    pass

@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ('customer_name', 'customer_cpf')
    pass

