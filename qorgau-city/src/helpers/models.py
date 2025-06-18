import uuid

from django.db import models


class CustomType(models.TextChoices):
    TOO = 'too', 'ТОО'
    AO = 'ao', 'АО'
    IP = 'ip', 'ИП'


class UUIDMixin(models.Model):
    uuid = models.UUIDField(verbose_name='uuid', default=uuid.uuid4, editable=False, primary_key=True)

    class Meta:
        abstract = True


class PathMixin(models.Model):
    path = models.FileField(verbose_name="путь", max_length=255, null=True, blank=True, upload_to="upload/%Y/%m/")

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    class Meta:
        abstract = True
