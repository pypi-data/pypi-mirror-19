from django.core.management import call_command


class DataModelsTestCaseMixin(object):
    datamodels = []

    @classmethod
    def setUpClass(cls):
        super(DataModelsTestCaseMixin, cls).setUpClass()
        if cls.datamodels:
            verbosity = getattr(cls, 'verbosity', 0)
            call_command('datamodels_loaddata', *cls.datamodels, verbosity=verbosity)
