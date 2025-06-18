from django.db import models


class Category(models.Model):
    """
    Модель категории объявления.
    """

    name = models.TextField(
        'Категория',
        blank=False, null=False
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=255, blank=True, null=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return f'{self.id}. {self.name[:20]}...'
