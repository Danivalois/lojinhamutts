from django import forms
from . import models
from django.core.exceptions import ValidationError

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
                'product_length': 'Comprimento do embalagem (cm):',
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
