# Generated by Django 5.0 on 2024-01-10 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auditlog_chenges'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auditlog',
            old_name='chenges',
            new_name='changes',
        ),
    ]
