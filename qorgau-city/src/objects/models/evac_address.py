from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

from helpers.models import TimestampMixin


class EvacAddress(
    TimestampMixin,
    models.Model
):
    """EvacAddresses."""

    address = models.CharField(max_length=255, verbose_name="адрес")
    file_path = models.FileField(
        max_length=2048,
        verbose_name="файл",
        null=True,
        blank=True,
        upload_to="public/%Y/%m/",
        storage=S3Boto3Storage(location='isec/')
    )
    qrcode_url = models.URLField(max_length=255, verbose_name="qrcode ссылка")

    class Meta:
        ordering = ('-id',)
        verbose_name = 'план эвакуации'
        verbose_name_plural = 'планы эвакуации'
