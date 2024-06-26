# Generated by Django 5.0 on 2024-01-07 12:56

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodmenu', '0010_alter_food_foodimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('phone_number', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Phone number must start with "09" and have 11 digits.', regex='^09\\d{9}$')])),
                ('is_approved', models.BooleanField(default=False)),
                ('rating', models.IntegerField()),
                ('comment', models.TextField()),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodmenu.food')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
