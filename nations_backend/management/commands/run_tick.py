from django.core.management.base import BaseCommand, CommandError
from ...models import Nation
from ...ticking import TickNation

class Command(BaseCommand):
    help = "Run one in-game tick."

    def handle(self, *args, **options):
        nations: list[Nation] = Nation.objects.all()
        
        [TickNation(nation).run_tick() for nation in nations]