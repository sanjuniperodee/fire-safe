from django.db import models

from .building import Building


class EscapeLadderImage(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='escape_ladder_images',
        verbose_name='Объект'
    )
    image = models.ImageField(
        upload_to='escape_ladder_images/',
        verbose_name='Изображение'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )

    class Meta:
        verbose_name = 'Изображение Эвакуационной Лестницы'
        verbose_name_plural = 'Изображения Эвакуационных Лестниц'

    def __str__(self):
        return f"{self.building} - {f'Image {self.id}'}"