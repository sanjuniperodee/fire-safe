from django.db import models

from helpers.models import TimestampMixin
from objects.models.building import Building


class DocumentHistory(
    TimestampMixin,
    models.Model
):
    action = models.TextField(null=True, blank=True)
    remark = models.TextField(null=True, blank=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='histories')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'история документа'
        verbose_name_plural = 'история документов'
