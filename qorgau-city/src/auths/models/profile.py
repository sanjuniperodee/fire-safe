import auths.validators as a_validators
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage

from .user import CustomUser


class Education(models.Model):
    class Degree(models.TextChoices):
        BACHELOR = 'Bachelor', 'Бакалавр'
        MASTERS = 'Masters', 'Магистр'
        OTHER = 'Other', 'Другое'
        UNSPECIFIED = 'Unspecified', 'Не указано'

        # Vocational = 'Vocational', 'Колледжное'
        # PostGraduate = 'PostGraduate', 'Аспирантура'
        # Doctoral = 'Doctoral', 'Докторский'

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='educations'
    )
    college_name = models.TextField(
        verbose_name='Информация об образовании'
    )
    year_start = models.IntegerField(
        verbose_name='Год начала'
    )
    year_end = models.IntegerField(
        verbose_name='Год окончания',
        blank=True,
        null=True
    )
    performing_now = models.BooleanField(
        default=False,
        verbose_name='Учусь здесь сейчас'
    )
    degree = models.CharField(
        max_length=20,
        choices=Degree.choices,
        default=Degree.UNSPECIFIED,
        help_text='Не указано степень образования',
        verbose_name='Степень образования',
        null=True,
        blank=True,
    )
    media = models.FileField(
        upload_to='education/diplomas/',
        storage=S3Boto3Storage(location='education/diplomas/'),
        validators=[a_validators.validate_documents_extension],
        verbose_name='Фото/Файл диплома',
        blank=True,
    )
    show_photo_to_clients = models.BooleanField(
        default=False,
        verbose_name='Показывать фото клиентам'
    )

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'

    def __str__(self):
        return f"{self.college_name} - {self.user.get_fullname}"


class Experience(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='experiences'
    )
    company_name = models.CharField(
        max_length=255,
        verbose_name='Название компании'
    )
    year_start = models.IntegerField(
        verbose_name='Год начала'
    )
    year_end = models.IntegerField(
        verbose_name='Год окончания',
        null=True, blank=True
    )
    performing_now = models.BooleanField(
        default=False,
        verbose_name='Работаю тут сейчас'
    )
    media = models.FileField(
        upload_to='experience/documents/',
        storage=S3Boto3Storage(location='experience/documents/'),
        validators=[a_validators.validate_documents_extension],
        verbose_name='Изображение/Файл документа'
    )

    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'

    def __str__(self):
        return f"{self.company_name} - {self.user.get_fullname}"


class Achievement(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='achievements'
    )
    certificate_name = models.CharField(
        max_length=255,
        verbose_name='Название достижения'
    )
    year_received = models.IntegerField(
        verbose_name='Год получения'
    )
    media = models.FileField(
        upload_to='achievements/documents/',
        storage=S3Boto3Storage(location='achievements/documents/'),
        validators=[a_validators.validate_documents_extension],
        verbose_name='Изображение/Файл документа достижения или грамоты'
    )
    show_photo_to_clients = models.BooleanField(
        default=False,
        verbose_name='Показывать фото клиентам'
    )

    class Meta:
        verbose_name = 'Достижение и грамоты'
        verbose_name_plural = 'Достижения и грамоты'

    def __str__(self):
        return f"{self.certificate_name} - {self.user.get_fullname}"


class OtherAchievement(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='other_achievements'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название других факторов которые показывают профессионализм'
    )
    year_start = models.IntegerField(
        verbose_name='Год начала'
    )
    year_end = models.IntegerField(
        verbose_name='Год окончания',
        null=True, blank=True
    )
    performing_now = models.BooleanField(
        default=False,
        verbose_name='Делаю другие достижения сейчас'
    )
    media = models.FileField(
        upload_to='other_professional_credentials/documents/',
        storage=S3Boto3Storage(location='other_professional_credentials/documents/'),
        validators=[a_validators.validate_documents_extension],
        verbose_name='Изображение/Файл документа других профессиональных навыков',
        null=True, blank=True
    )
    show_photo_to_clients = models.BooleanField(
        default=False,
        verbose_name='Показывать фото клиентам'
    )

    class Meta:
        verbose_name = 'Другие факторы показывающие профессионализм'
        verbose_name_plural = 'Другие факторы показывающие профессионализм'

    def __str__(self):
        return f"{self.name} - {self.user.get_fullname}"
