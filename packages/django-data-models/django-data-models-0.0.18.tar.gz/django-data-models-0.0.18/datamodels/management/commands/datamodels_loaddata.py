import os
import warnings

import django.apps
from django.conf import settings
from django.core import serializers
from django.core.management import call_command, CommandError
from django.core.management.base import BaseCommand
from django.core.management.commands.loaddata import Command as LoaddataCommand, humanize
from django.db import router, DatabaseError, IntegrityError
from django.utils.encoding import force_text

from ...models import DataModel

LOADDATA_COMMAND = getattr(settings, 'DATAMODELS_LOADDATA_COMMAND', 'loaddata')


class Command(BaseCommand):
    help = 'Loads data for all DataModels'
    verbosity = 1

    def handle(self, *args, **options):
        self.verbosity = options['verbosity']

        loaded_models = []

        data_models = [model for model in django.apps.apps.get_models() if issubclass(model, DataModel)]
        for model in data_models:
            self.load_model_fixtures(model, loaded_models=loaded_models)

    def load_model_fixtures(self, model, loaded_models):
        if model in loaded_models:
            return

        self.load_dependencies(model, loaded_models)

        fixtures = getattr(model.DataModelMeta, 'fixtures', None) or []
        for fixture in fixtures:
            if self.verbosity >= 1:
                print("Loading %s..." % fixture)
            call_command(LOADDATA_COMMAND, fixture, verbosity=self.verbosity, skip_checks=True)
            if self.verbosity >= 1:
                print('')

        default_fixtures = getattr(model.DataModelMeta, 'default_fixtures', None) or []
        for fixture in default_fixtures:
            if self.verbosity >= 1:
                print("Loading default %s..." % fixture)
            call_command(DefaultOnlyLoaddataComand(), fixture, verbosity=self.verbosity, skip_checks=True)
            if self.verbosity >= 1:
                print('')

        loaded_models.append(model)

    def load_dependencies(self, model, loaded_models):
        if not issubclass(model, DataModel):
            raise '%s was set as datamodel dependency, but it\'s not a DataModel' % (unicode(model))

        dependencies = getattr(model.DataModelMeta, 'dependencies', None) or []
        for dep_model_str in dependencies:
            app_label, model_name = dep_model_str.split('.')
            dep_model = django.apps.apps.get_model(model_name=model_name, app_label=app_label)
            self.load_model_fixtures(dep_model, loaded_models=loaded_models)


class DefaultOnlyLoaddataComand(LoaddataCommand):
    def load_label(self, fixture_label):
        """
        Loads fixtures files for a given label.
        """
        show_progress = self.verbosity >= 3
        for fixture_file, fixture_dir, fixture_name in self.find_fixtures(fixture_label):
            _, ser_fmt, cmp_fmt = self.parse_name(os.path.basename(fixture_file))
            open_method, mode = self.compression_formats[cmp_fmt]
            fixture = open_method(fixture_file, mode)
            try:
                self.fixture_count += 1
                objects_in_fixture = 0
                loaded_objects_in_fixture = 0
                if self.verbosity >= 2:
                    self.stdout.write(
                        "Installing %s fixture '%s' from %s."
                        % (ser_fmt, fixture_name, humanize(fixture_dir))
                    )
                objects = serializers.deserialize(
                    ser_fmt, fixture, using=self.using, ignorenonexistent=self.ignore,
                )

                for obj in objects:
                    objects_in_fixture += 1
                    if router.allow_migrate_model(self.using, obj.object.__class__):
                        self.models.add(obj.object.__class__)
                        try:
                            if obj.object.__class__.objects.filter(id=obj.object.id).exists():
                                continue
                            loaded_objects_in_fixture += 1
                            obj.save(using=self.using)
                            if show_progress:
                                self.stdout.write(
                                    '\rProcessed %i object(s).' % loaded_objects_in_fixture,
                                    ending=''
                                )
                        except (DatabaseError, IntegrityError) as e:
                            e.args = ("Could not load %(app_label)s.%(object_name)s(pk=%(pk)s): %(error_msg)s" % {
                                'app_label': obj.object._meta.app_label,
                                'object_name': obj.object._meta.object_name,
                                'pk': obj.object.pk,
                                'error_msg': force_text(e)
                            },)
                            raise
                if objects and show_progress:
                    self.stdout.write('')  # add a newline after progress indicator
                self.loaded_object_count += loaded_objects_in_fixture
                self.fixture_object_count += objects_in_fixture
            except Exception as e:
                if not isinstance(e, CommandError):
                    e.args = ("Problem installing fixture '%s': %s" % (fixture_file, e),)
                raise
            finally:
                fixture.close()

            # Warn if the fixture we loaded contains 0 objects.
            if objects_in_fixture == 0:
                warnings.warn(
                    "No fixture data found for '%s'. (File format may be "
                    "invalid.)" % fixture_name,
                    RuntimeWarning
                )
