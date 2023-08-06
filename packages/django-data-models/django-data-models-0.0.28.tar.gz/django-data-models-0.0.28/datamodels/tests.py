from django.core.management import call_command


class DataModelTestCaseMixin(object):
    datamodels = []

    @classmethod
    def setUpClass(cls):
        super(DataModelTestCaseMixin, cls).setUpClass()
        if cls.datamodels:
            verbosity = getattr(cls, 'verbosity', 0)
            call_command('datamodels_loaddata', *cls.datamodels, verbosity=verbosity)
