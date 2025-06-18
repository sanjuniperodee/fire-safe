from django.db import models

from helpers.models import TimestampMixin


class FAQ(
    TimestampMixin,
    models.Model
):
    """Fag model."""

    question = models.TextField(verbose_name="вопрос")
    answer = models.TextField(verbose_name="ответ")

    class Meta:
        ordering = ('-id',)
