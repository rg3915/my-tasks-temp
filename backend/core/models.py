import uuid

from django.db import models


class UuidModel(models.Model):
    slug = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        'criado em',
        auto_now_add=True,
        auto_now=False
    )
    modified = models.DateTimeField(
        'modificado em',
        auto_now_add=False,
        auto_now=True
    )

    class Meta:
        abstract = True


class Active(models.Model):
    active = models.BooleanField('ativo', default=True)

    class Meta:
        abstract = True
