# Generated by Django 5.1.6 on 2025-03-09 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_order_leadtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_payment_ID',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
