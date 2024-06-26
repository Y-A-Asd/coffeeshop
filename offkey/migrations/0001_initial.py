# Generated by Django 5.0 on 2024-01-09 11:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offkey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('valid_from', models.DateField()),
                ('valid_to', models.DateField()),
                ('discount', models.DecimalField(decimal_places=0, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('active', models.BooleanField()),
            ],
        ),
    ]
