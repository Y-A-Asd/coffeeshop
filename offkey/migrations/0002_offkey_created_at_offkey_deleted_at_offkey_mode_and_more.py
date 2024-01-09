# Generated by Django 5.0 on 2024-01-09 11:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offkey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offkey',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='offkey',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='offkey',
            name='mode',
            field=models.CharField(choices=[('OT', 'OneTimeUse'), ('TE', 'MultiTimeUse')], default='TE', max_length=2),
        ),
        migrations.AddField(
            model_name='offkey',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='offkey',
            name='valid_to',
            field=models.DateField(blank=True, null=True),
        ),
    ]
