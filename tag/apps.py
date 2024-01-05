from django.apps import AppConfig


class TagConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tag'

    def ready(self):
        import core.signals
        import tag.signals