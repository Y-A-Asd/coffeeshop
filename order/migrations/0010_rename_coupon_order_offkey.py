# Generated by Django 5.0 on 2024-01-09 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_order_coupon_order_discount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='coupon',
            new_name='offkey',
        ),
    ]
