import django.apps
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from ...models import DataModel

LOADDATA_COMMAND = getattr(settings, 'DATAMODELS_LOADDATA_COMMAND', 'loaddata')


class Command(BaseCommand):
    help = 'Loads data for all DataModels'
    verbosity = 1

    def handle(self, *args, **options):
        self.verbosity = options['verbosity']
        for model in django.apps.apps.get_models():
            if not issubclass(model, DataModel):
                continue

            fixtures = getattr(model.DataModelMeta, 'fixtures', None)
            if not fixtures:
                continue

            for fixture in fixtures:
                if self.verbosity >= 2:
                    print("Loading %s..." % fixture)
                call_command(LOADDATA_COMMAND, fixture, verbosity=self.verbosity, skip_checks=True)

                if self.verbosity >= 2:
                    print('')
