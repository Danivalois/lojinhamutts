# Generated by Django 5.1.6 on 2025-03-09 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_order_pmt_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_site_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
