from django.db import models
from django.core.validators import RegexValidator

from auths.models import CustomUser
from objects import (SubBuildingType, Rating, ObjectMainOrganizationType,
                     LightingType, VentilationType, HeatingType, SecurityType, StairsClassificationType, )
from objects.models.document import Document, OrganizationType, DocumentKey
from specifications.models import (
    ExternalWallMaterialChoice, InnerWallMaterialChoice,
    RoofChoice, StairsMaterialChoice,
    StairsTypeChoice, LightingTypeChoice,
    VentilationTypeChoice, HeatingChoice,
    SecurityChoice, StairsClassificationChoice,
)

from helpers.models import CustomType, TimestampMixin


class Building(
    TimestampMixin,
    models.Model
):
    """Object building model."""

    organization_type = models.ForeignKey(
        OrganizationType,
        verbose_name='Главный Тип организации',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    organization_sub_type = models.CharField(
        'Тип организации',
        max_length=200,
        # choices=ObjectMainOrganizationType.choices,
        # default=ObjectMainOrganizationType.Commercial_Organizations,
        null=True, blank=True,
    )
    organization_optional_type = models.CharField(
        'Под тип организации(Optional)',
        max_length=200,
        null=True, blank=True,
    )
    organization_characteristics = models.CharField(
        'Характеристики организации',
        max_length=200,
        null=True, blank=True,
    )
    organization_name = models.TextField(
        'Название организации',
        null=True, blank=True
    )
    iin = models.CharField(
        'ИИН',
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{12}$',
                message='IIN must be exactly 12 digits.'
            )
        ]
    )
    owner = models.ForeignKey(
        CustomUser,
        # on_delete=models.SET_NULL,
        on_delete=models.CASCADE,
        verbose_name='собственник',
        null=True, blank=True
    )
    inspector = models.ForeignKey(
        CustomUser, verbose_name='Инспектор',
        related_name='inspected_buildings',
        on_delete=models.SET_NULL,
        blank=True, null=True, default=None
    )
    address = models.TextField('Адрес')
    rating = models.CharField(
        'Рейтинг',
        max_length=1,
        choices=Rating.choices,
        null=True, blank=True
    )
    documents = models.ManyToManyField(
        Document,
        verbose_name='Главы документов',
        blank=True
    )
    document_keys = models.ManyToManyField(
        DocumentKey,
        verbose_name='Документы',
        blank=True
    )
    # full_name = models.CharField(
    #     verbose_name='Полное имя',
    #     max_length=255,
    #     null=True, blank=True
    # )
    escape_ladder = models.BooleanField(
        default=False,
        verbose_name='Эвакуационная лестница (имеется)',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    # def __str__(self):
    #     return '{display_value} {value}'.format(
    #         value=self.organization_name,
    #         display_value=self.get_organization_type_display(),
    #     )
    def __str__(self):
        return '{display_value} {value}'.format(
            value=self.organization_name or '',
            display_value=self.organization_type or '',
        )


class SubBuilding(
    TimestampMixin,
    models.Model
):
    """Модель здания/сооружения, относящегося к объекту."""

    building = models.ForeignKey(
        Building,
        related_name='subbuildings',
        verbose_name='Головной объект',
        on_delete=models.CASCADE
    )
    subbuilding_type = models.CharField(
        'Главный Тип здания/сооружения/помещения/иной конструкции',
        max_length=255,
        null=True, blank=True,
    )
    subbuilding_subtype = models.CharField(
        'Тип здания/сооружения/помещения/иной конструкции',
        null=True, blank=True,
    )
    subbuilding_optional_subtype_type = models.CharField(
        'Под тип здания/сооружения/помещения/иной конструкции(Optional)',
        max_length=200,
        null=True, blank=True,
    )
    subbuilding_characteristics = models.CharField(
        'Характеристики подздания',
        max_length=200,
        null=True, blank=True,
    )
    title = models.CharField(
        'Наименование',
        null=True, blank=True
    )
    functional_purpose = models.CharField(
        'Предназначение',
        max_length=255,
        null=True, blank=True
    )
    date_commissioning = models.DateField(
        'Дата ввода в эксплуатацию',
        null=True, blank=True
    )
    fire_resistance_rating = models.CharField(
        'Степень огнестойкости',
        # frontend choiceField
        max_length=600,
        null=True, blank=True
    )
    structural_po_class = models.CharField(
        'Класс конструктивной ПО',
        # frontend choiceField
        max_length=255,
        null=True, blank=True
    )
    functional_po_class = models.CharField(
        'Класс функциональной ПО',
        # frontend choiceField
        max_length=255,
        null=True, blank=True
    )
    rating = models.CharField(
        'Рейтинг',
        max_length=1,
        choices=Rating.choices,
        null=True, blank=True
    )
    change_functional_purpose_date = models.DateField(
        'Дата изменения функционального назначения',
        null=True, blank=True
    )
    floor_number = models.PositiveSmallIntegerField(
        'Этаж',
        default=1,
        null=True, blank=True
    )
    total_floors = models.PositiveSmallIntegerField(
        'Всего этажей',
        default=1,
        null=True, blank=True
    )
    building_foundation = models.TextField(
        'Фундамент здания',
        null=True, blank=True
    )
    external_walls_material = models.ManyToManyField(
        ExternalWallMaterialChoice,
        verbose_name='Материал наружных стен',
        related_name='subbuildings_external',
    )
    inner_walls_material = models.ManyToManyField(
        InnerWallMaterialChoice,
        verbose_name='Внутренние стены и перегородки (материал)',
        related_name='subbuildings_internal',
    )
    roof = models.ManyToManyField(
        RoofChoice,
        verbose_name='Кровля (тип, материал)',
        related_name='subbuildings_roof',
    )
    stairs_material = models.ManyToManyField(
        StairsMaterialChoice,
        verbose_name='Лестницы (материал)',
        related_name='subbuildings_stairs_material',
    )
    stairs_type = models.ManyToManyField(
        StairsTypeChoice,
        verbose_name='Лестницы (тип)',
        related_name='subbuildings_stairs_type',
    )
    stairs_classification = models.ManyToManyField(
        StairsClassificationChoice,
        verbose_name='Классификация лестницы',
        related_name='subbuildings_stairs_classification',
    )

    building_height = models.FloatField(
        'Высота здания, м',
        null=True, blank=True
    )
    area = models.FloatField(
        'Общая площадь, м^2',
        null=True, blank=True
    )
    volume = models.FloatField(
        'Объем здания, м^3',
        null=True, blank=True
    )
    lighting = models.ManyToManyField(
        LightingTypeChoice,
        verbose_name='Освещение',
        related_name='subbuildings_lighting_type',
    )
    emergency_lighting = models.BooleanField(
        default=False,
        verbose_name='Аварийное освещение (Имеется)',
    )
    ventilation = models.ManyToManyField(
        VentilationTypeChoice,
        verbose_name='Вентиляция',
        related_name='subbuildings_ventilation_type',
    )
    heating = models.ManyToManyField(
        HeatingChoice,
        verbose_name='Отопление',
        related_name='subbuildings_heating',
    )
    security = models.ManyToManyField(
        SecurityChoice,
        verbose_name='Объект охраняется',
        related_name='subbuildings_security',
    )
    year_construction_reconstruction = models.PositiveSmallIntegerField(
        'Год постройки/реконструкции',
        null=True, blank=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Здание/Сооружение'
        verbose_name_plural = 'Здания/Сооружения'

    def __str__(self):
        return f'{self.building} - {self.title}'


class BuildingImage(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Объект'
    )
    image = models.ImageField(
        upload_to='building_images/',
        verbose_name='Изображение'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )

    class Meta:
        verbose_name = 'Изображение объекта'
        verbose_name_plural = 'Изображения объектов'

    def __str__(self):
        return f"{self.building} - {f'Image {self.id}'}"


class SubBuildingImage(models.Model):
    subbuilding = models.ForeignKey(
        SubBuilding,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Здание/Сооружение'
    )
    image = models.ImageField(
        upload_to='subbuilding_images/',
        verbose_name='Изображение'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки'
    )

    class Meta:
        verbose_name = 'Изображение здания/сооружения'
        verbose_name_plural = 'Изображения зданий/сооружений'

    def __str__(self):
        # return f"{self.subbuilding} - {self.caption or f'Image {self.id}'}"
        return f"{self.subbuilding} - {f'Image {self.id}'}"


class BuildingPDFDocument(TimestampMixin, models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='pdf_documents'
    )
    file = models.FileField(
        upload_to='building_pdfs/',
        verbose_name='PDF Document'
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Building PDF Document'
        verbose_name_plural = 'Building PDF Documents'

    def __str__(self):
        return f"PDF for {self.building} - {self.created_at}"