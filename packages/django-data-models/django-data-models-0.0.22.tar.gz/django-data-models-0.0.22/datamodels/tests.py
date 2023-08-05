from django.core.management import call_command
from django.test import TestCase


class DataModelTestCaseMixin(TestCase):

    datamodels = []

    def setUp(self):
        if self.datamodels:
            verbosity = getattr(self, 'verbosity', 0)
            call_command('datamodels_loaddata', *self.datamodels, verbosity=verbosity)
        super(DataModelTestCaseMixin, self).setUp()
