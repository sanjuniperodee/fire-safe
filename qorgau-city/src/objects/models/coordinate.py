from django.db import models

from objects.models.building import Building
from helpers.models import TimestampMixin


class BuildingCoordinates(
    TimestampMixin,
    models.Model
):
    # lat = models.FloatField()
    # lng = models.FloatField()
    # building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='coordinates')
    building = models.OneToOneField(
        'Building',
        on_delete=models.CASCADE,
        related_name='coordinates',
        verbose_name='Объект'
    )
    lat = models.DecimalField(
        'Широта',
        # max_digits=9,
        # decimal_places=6
        max_digits=40,
        decimal_places=20,
    )
    lng = models.DecimalField(
        'Долгота',
        # max_digits=9,
        # decimal_places=6
        max_digits=40,
        decimal_places=20
    )

    class Meta:
        ordering = ('-id',)
        # verbose_name = 'Координата здания/сооружения'
        # verbose_name_plural = 'Координаты здании/сооружении'
        verbose_name = 'Координата обьекта'
        verbose_name_plural = 'Координаты обьектов'

    def __str__(self):
        return f"Координаты для обьекта: {self.building}"
