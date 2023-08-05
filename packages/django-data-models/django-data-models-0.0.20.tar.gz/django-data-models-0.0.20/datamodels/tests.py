from django.core.management import call_command
from django.test import TestCase


class DataModelTestCaseMixin(TestCase):

    def setUp(self):
        call_command('datamodels_loaddata', verbosity=0)
        super(DataModelTestCaseMixin, self).setUp()
