# Generated by Django 5.1.6 on 2025-03-29 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_product_product_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image_url',
            field=models.CharField(blank=True, max_length=900, null=True),
        ),
    ]
