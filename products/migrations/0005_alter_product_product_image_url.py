# Generated by Django 5.1.6 on 2025-03-28 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_product_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image_url',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
