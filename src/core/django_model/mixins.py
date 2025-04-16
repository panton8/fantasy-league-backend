import uuid

from django.db import models

__all__ = (
    'CreatedUpdatedAt',
    'UuidPk'
)


class CreatedUpdatedAt(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['pk', ]


class UuidPk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
