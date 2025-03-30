from django.contrib import admin
from .models import Product, Category
from import_export.admin import ExportMixin, ImportExportModelAdmin
from .models import Product

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('id', 'product_code', 'product_short_description')
    pass

admin.site.register(Category)
