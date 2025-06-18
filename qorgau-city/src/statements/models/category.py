from django.db import models

from auths.models import (
    Category,
)
from .statement import (
    Statement,
)


class StatementCategory(models.Model):
    statement = models.ForeignKey(
        Statement,
        verbose_name='Заявка',
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория заявки'
        verbose_name_plural = 'Категории заявки'
