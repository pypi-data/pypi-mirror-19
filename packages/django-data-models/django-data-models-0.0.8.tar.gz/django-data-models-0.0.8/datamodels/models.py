from __future__ import unicode_literals

from django.db import models


class DataModelsReadOnlyException(Exception):
    pass


class DataModelQuerySet(models.QuerySet):
    def delete(self):
        raise DataModelsReadOnlyException("You can't delete DataModel objects")

    def _raw_delete(self, *args, **kwargs):
        raise DataModelsReadOnlyException("You can't delete DataModel objects")

    def update(self, *args, **kwargs):
        raise DataModelsReadOnlyException("You can't update DataModel objects")

    def _update(self, *args, **kwargs):
        raise DataModelsReadOnlyException("You can't update DataModel objects")

    def select_for_update(self, *args, **kwargs):
        raise DataModelsReadOnlyException("You can't update DataModel objects")


class DataModel(models.Model):
    objects = DataModelQuerySet.as_manager()

    class DataModelMeta:
        fixtures = None
        default_fixtures = None
        readonly = True

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        raise DataModelsReadOnlyException("You can't update or create DataModel objects")

    def delete(self, *args, **kwargs):
        raise DataModelsReadOnlyException("You can't delete DataModel objects")
