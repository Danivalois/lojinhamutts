from django import forms
from . import models
from django.core.exceptions import ValidationError
from .models import Product

class CreateProduct(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = [
                'product_code',
                'product_short_description',
                'product_description_long',
                'product_category',
                'product_unit_price',
                'product_stock',
                'product_thumbnail_url',
                'product_brand',
                'product_sku',
                'product_weight',
                'product_dimensions',
                'product_length',
                'product_width',
                'product_height',
                'product_image_url',
                'product_is_active',
        ]
        labels = {
                'product_code': 'Código do Produto:',
                'product_short_description': 'Descrição Curta:',
                'product_description_long': 'Descrição Longa:',
                'product_category': 'Categoria:',
                'product_unit_price': 'Preço Unitário',
                'product_stock': 'Qtd.em Estoque:',
                'product_thumbnail_url': 'URL Thumbnail:',
                'product_brand': 'Marca:',
                'product_sku': 'SKU:',
                'product_weight': 'Peso (prod. + embalagem em kg):',
                'product_dimensions': 'Dimensões do Produto (cm):',
                'product_height': 'Altura da embalagem (cm):',
                'product_width': 'Largura da embalagem (cm):',
                'product_length': 'Comprimento da embalagem (cm):',
                'product_image_url': 'Imagem do Produto:',
                'product_is_active': 'Produto está ativo? :',
                }

class EditProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = [
                'product_code',
                'product_short_description',
                'product_description_long',
                'product_category',
                'product_unit_price',
                'product_stock',
                'product_thumbnail_url',
                'product_brand',
                'product_sku',
                'product_weight',
                'product_dimensions',
                'product_length',
                'product_width',
                'product_height',
                'product_image_url',
                'product_is_active',
        ]
        labels = {
                'product_code': 'Código do Produto:',
                'product_short_description': 'Descrição Curta:',
                'product_description_long': 'Descrição Longa:',
                'product_category': 'Categoria:',
                'product_unit_price': 'Preço Unitário',
                'product_stock': 'Qtd.em Estoque:',
                'product_thumbnail_url': 'URL Thumbnail:',
                'product_brand': 'Marca:',
                'product_sku': 'SKU:',
                'product_weight': 'Peso (prod. + embalagem em kg):',
                'product_dimensions': 'Dimensões do Produto (cm):',
                'product_height': 'Altura da embalagem (cm):',
                'product_width': 'Largura da embalagem (cm):',
                'product_length': 'Comprimento do embalagem (cm):',
                'product_image_url': 'Imagem do Produto:',
                'product_is_active': 'Produto está ativo? :',
                }


class ProductForm(forms.ModelForm):
    image_upload = forms.ImageField(required=False)

    class Meta:
        model = Product
        fields = [
                'product_code',
                'product_short_description',
                'product_description_long',
                'product_category',
                'product_unit_price',
                'product_stock',
                'product_thumbnail_url',
                'product_brand',
                'product_sku',
                'product_weight',
                'product_dimensions',
                'product_length',
                'product_width',
                'product_height',
                'product_image_url',
                'product_is_active',
        ]
        labels = {
            'product_code': 'Código do Produto:',
            'product_short_description': 'Descrição Curta:',
            'product_description_long': 'Descrição Longa:',
            'product_category': 'Categoria:',
            'product_unit_price': 'Preço Unitário',
            'product_stock': 'Qtd.em Estoque:',
            'product_thumbnail_url': 'URL Thumbnail:',
            'product_brand': 'Marca:',
            'product_sku': 'SKU:',
            'product_weight': 'Peso (prod. + embalagem em kg):',
            'product_dimensions': 'Dimensões do Produto (cm):',
            'product_height': 'Altura da embalagem (cm):',
            'product_width': 'Largura da embalagem (cm):',
            'product_length': 'Comprimento do embalagem (cm):',
            'product_image_url': 'Imagem do Produto:',
            'product_is_active': 'Produto está ativo? :',
            }

    def save(self, commit=True):
        instance = super().save(commit=False)

        image = self.cleaned_data.get('image_upload')
        if image:
            from utils.supabase_upload import upload_image_to_supabase
            url = upload_image_to_supabase(image, image.name)
            instance.product_image_url = url

        if commit:
            instance.save()
        return instance

