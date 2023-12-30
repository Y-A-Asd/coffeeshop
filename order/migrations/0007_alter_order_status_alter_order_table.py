# Generated by Django 5.0 on 2023-12-30 18:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_orderitem_price'),
        ('tables', '0003_alter_table_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('W', 'Waiting'), ('C', 'Canceled'), ('P', 'Preparation'), ('T', 'Transmission'), ('F', 'Finished')], default='W', max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='tables.table'),
        ),
    ]
