# Generated by Django 5.0 on 2024-01-09 22:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offkey', '0002_offkey_created_at_offkey_deleted_at_offkey_mode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offkey',
            name='discount',
            field=models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
