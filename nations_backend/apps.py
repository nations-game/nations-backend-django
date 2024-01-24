from django.db.models.signals import post_migrate
from django.apps import AppConfig



class NationsConfig(AppConfig):
    name = "nations_backend"
    verbose_name = "Nations Backend"

    def ready(self):
        ...