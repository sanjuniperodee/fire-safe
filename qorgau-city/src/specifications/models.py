from django.db import models

from specifications import StairsClassificationType


class ExternalWallMaterialChoice(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Материал наружных стен'
        verbose_name_plural = 'Материалы наружных стен'

    def __str__(self):
        return self.name


class InnerWallMaterialChoice(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Внутренние стены и перегородки'
        verbose_name_plural = 'Внутренние стены и перегородки'

    def __str__(self):
        return self.name


class RoofChoice(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тип кровли'
        verbose_name_plural = 'Типы кровли'

    def __str__(self):
        return self.name


class StairsMaterialChoice(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Материал лестницы'
        verbose_name_plural = 'Материалы лестниц'

    def __str__(self):
        return self.name


class StairsTypeChoice(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тип лестницы'
        verbose_name_plural = 'Типы лестниц'

    def __str__(self):
        return self.name


class LightingTypeChoice(models.Model):
    # name = models.CharField(
    #     choices=LightingType.choices,
    #     default=LightingType.NATURAL_LIGHTING,
    # )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Освещение'
        verbose_name_plural = 'Освещения'

    def __str__(self):
        return self.name


class VentilationTypeChoice(models.Model):
    # name = models.CharField(
    #     choices=VentilationType.choices,
    #     default=VentilationType.NATURAL_VENTILATION,
    # )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Вентиляция'
        verbose_name_plural = 'Вентиляции'

    def __str__(self):
        return self.name


class HeatingChoice(models.Model):
    # name = models.CharField(
    #     choices=HeatingType.choices,
    #     default=HeatingType.AUTONOMOUS,
    # )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Отопление'
        verbose_name_plural = 'Отопление'

    def __str__(self):
        return self.name


class SecurityChoice(models.Model):
    # name = models.CharField(
    #     choices=SecurityType.choices,
    #     default=SecurityType.NOT_GUARDED,
    # )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Объект охраняется'
        verbose_name_plural = 'Объект охраняется'

    def __str__(self):
        return self.name


class StairsClassificationChoice(models.Model):
    name = models.CharField(
        max_length=2,
        choices=StairsClassificationType.choices,
        default=StairsClassificationType.N_1,
    )
    description = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = 'Классификация Лестниц(Н1,Н2,L1,L2,L3)'
        verbose_name_plural = 'Классификация Лестниц(Н1,Н2,L1,L2,L3)'

    def save(self, *args, **kwargs):
        self.description = dict(StairsClassificationType.choices)[self.name]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.description}"