from django.db import models
from django.core.validators import RegexValidator

from helpers.models import TimestampMixin
from auths.models import CustomUser
from objects.models.building import Building


class BuldingInfo(
    TimestampMixin,
    models.Model
):
    """ObjectInfo model."""

    organization_name = models.CharField(max_length=255, verbose_name="название")
    iin = models.CharField(
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{12}$',
                message="IIN must be exactly 12 digits."
            )
        ],
        verbose_name="иин"
    )
    address = models.TextField(verbose_name="адрес")
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='building_info')
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='building_info')
    functional_purpose = models.CharField(max_length=255, null=True, blank=True)
    date_commissioning = models.DateField(null=True, blank=True)
    fire_resistance_rating = models.CharField(max_length=255, null=True, blank=True)
    structural_po_class = models.CharField(max_length=255, null=True, blank=True)
    functional_po_class = models.CharField(max_length=255, null=True, blank=True)
    number_floor = models.IntegerField(default=1)
    building_height = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=255, null=True, blank=True)
    volume = models.CharField(max_length=255, null=True, blank=True)
    year_construction_reconstruction = models.CharField(max_length=12, null=True, blank=True)
    change_functional_purpose_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'информация объекта'
        verbose_name_plural = 'информация объектов'
