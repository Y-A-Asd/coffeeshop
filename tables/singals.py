from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from tables.models import Table


@receiver(post_migrate, sender=apps.get_app_config('tables'))
def create_default_tables(sender, app_config, **kwargs):
    if not Table.objects.filter(status='T').exists():
        Table.objects.create(number=0, status='T')
