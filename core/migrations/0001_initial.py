# Generated by Django 5.0 on 2023-12-19 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('foodmenu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodTagModel',
            fields=[
                ('food_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='foodmenu.food')),
            ],
            bases=('foodmenu.food',),
        ),
    ]
