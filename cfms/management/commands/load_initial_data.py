from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Загружает начальные справочники (статусы, типы, категории, подкатегории) для ДДС."

    def handle(self, *args, **options):
        call_command("loaddata", "cfms/fixtures/initial_data.json")
        self.stdout.write(self.style.SUCCESS("Начальные справочники успешно загружены!"))
