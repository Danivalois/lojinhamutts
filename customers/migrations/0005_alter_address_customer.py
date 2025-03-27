# Generated by Django 5.1.6 on 2025-03-02 22:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_alter_address_customer_zip_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='customers.customer'),
        ),
    ]
