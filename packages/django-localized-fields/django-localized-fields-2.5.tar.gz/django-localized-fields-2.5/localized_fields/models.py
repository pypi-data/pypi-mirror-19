from django.db import models, transaction
from django.db.utils import IntegrityError
from django.conf import settings

from .fields import LocalizedField
from .localized_value import LocalizedValue


class LocalizedModel(models.Model):
    """A model that contains localized fields."""

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        """Initializes a new instance of :see:LocalizedModel.

        Here we set all the fields that are of :see:LocalizedField
        to an instance of :see:LocalizedValue in case they are none
        so that the user doesn't explicitely have to do so."""

        super(LocalizedModel, self).__init__(*args, **kwargs)

        for field in self._meta.get_fields():
            if not isinstance(field, LocalizedField):
                continue

            value = getattr(self, field.name, None)

            if not isinstance(value, LocalizedValue):
                if isinstance(value, dict):
                    value = LocalizedValue(value)
                else:
                    value = LocalizedValue()

            setattr(self, field.name, value)

    def save(self, *args, **kwargs):
        """Saves this model instance to the database."""

        max_retries = getattr(
            settings,
            'LOCALIZED_FIELDS_MAX_RETRIES',
            100
        )

        if not hasattr(self, 'retries'):
            self.retries = 0

        with transaction.atomic():
            try:
                return super(LocalizedModel, self).save(*args, **kwargs)
            except IntegrityError as ex:
                # this is as retarded as it looks, there's no
                # way we can put the retry logic inside the slug
                # field class... we can also not only catch exceptions
                # that apply to slug fields... so yea.. this is as
                # retarded as it gets... i am sorry :(
                if 'slug' not in str(ex):
                    raise ex

                if self.retries >= max_retries:
                    raise ex

        self.retries += 1
        return self.save()
