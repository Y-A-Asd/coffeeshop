# Generated by Django 5.0 on 2024-01-11 15:40

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0004_alter_reservation_status'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='reservation',
            managers=[
                ('defman', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='table',
            managers=[
                ('defman', django.db.models.manager.Manager()),
            ],
        ),
    ]
