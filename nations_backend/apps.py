from django.db.models.signals import post_migrate
from django.apps import AppConfig



class NationsConfig(AppConfig):
    name = "nations_backend"
    verbose_name = "Nations Backend"

    def ready(self):
        self.create_factory_types()

    def create_factory_types(self) -> None:
        from .models import FactoryType
        
        if not FactoryType.objects.filter(name="Farm").exists():
            FactoryType.objects.create(
                name="Farm",
                commodity="food"
            )

        if not FactoryType.objects.filter(name="Clothes Factory").exists():
            FactoryType.objects.create(
                name="Clothes Factory",
                commodity="consumer_goods"
            )

        if not FactoryType.objects.filter(name="Hydro Power Plant").exists():
            FactoryType.objects.create(
                name="Hydro Power Plant",
                commodity="power"
            )