import gzip
import json
import os

import django.apps
import yaml
from django.core import serializers
from django.core.management.base import BaseCommand
from django.core.management.commands.loaddata import Command as LoaddataCommand, SingleZipReader
from django.db import DEFAULT_DB_ALIAS

from ...models import DataModel


class Command(BaseCommand):
    help = 'Loads data for all DataModels'
    verbosity = 1

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='labels', nargs='*',
            help='Module paths to datamodel; can be appname or appname.ModelName'
        )

    def handle(self, *args, **options):
        print('Checking datamodels...')
        self.check_datamodels_meta_exists()
        self.check_meta_has_fixtures()
        self.check_datamodels_inheritance()
        self.check_fixtures_for_correct_content_type()

    def check_meta_has_fixtures(self):
        for model in self.get_data_models():
            meta = getattr(model, 'DataModelMeta', None)
            fixtures = getattr(meta, 'fixtures', [])
            default_fixtures = getattr(meta, 'default_fixtures', [])
            if not fixtures and not default_fixtures:
                print("  %s.DataModelMeta doesn't use fixtures or default_fixtures " % model._meta.label)

    def check_datamodels_meta_exists(self):
        for model in self.get_data_models():
            meta = getattr(model, 'DataModelMeta', None)
            if meta is None:
                print("  %s doesn't have DataModelMeta" % model._meta.label)
                continue

    def check_datamodels_inheritance(self):
        for model in django.apps.apps.get_models():
            if hasattr(model, 'DataModelMeta') and not issubclass(model, DataModel):
                print("  %s has DataModelMeta but it's not a child of DataModel" % model._meta.label)

    def check_fixtures_for_correct_content_type(self):
        for model in self.get_data_models():
            meta = getattr(model, 'DataModelMeta', None)
            fixtures = getattr(meta, 'fixtures', [])
            default_fixtures = getattr(meta, 'default_fixtures', [])
            loaddata_command = self.get_loaddata_command_instance()

            for fixture_label in fixtures + default_fixtures:
                for fixture_file, fixture_dir, fixture_name in loaddata_command.find_fixtures(fixture_label):
                    _, ser_fmt, cmp_fmt = loaddata_command.parse_name(os.path.basename(fixture_file))
                    open_method, mode = loaddata_command.compression_formats[cmp_fmt]
                    fixture = open_method(fixture_file, mode)

                    objects = {
                        'json': json.loads,
                        'yaml': yaml.safe_load
                    }[ser_fmt](fixture.read())

                    for obj in objects:

                        if obj['model'] != model._meta.label.lower():
                            print('%s have a datafixture %s which have an object with different content type %s' % (
                                model._meta.label, fixture_label, obj['model']
                            ))


    def get_loaddata_command_instance(self):
        loaddata_command = LoaddataCommand()
        loaddata_command.using = DEFAULT_DB_ALIAS
        loaddata_command.serialization_formats = serializers.get_public_serializer_formats()
        loaddata_command.compression_formats = {
            None: (open, 'rb'),
            'gz': (gzip.GzipFile, 'rb'),
            'zip': (SingleZipReader, 'r'),
        }
        loaddata_command.verbosity = 0
        loaddata_command.app_label = None
        return loaddata_command

    def get_data_models(self):
        return [model for model in django.apps.apps.get_models() if issubclass(model, DataModel)]
