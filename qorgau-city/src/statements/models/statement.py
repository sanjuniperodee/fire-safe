from django.db import models

import auths.validators as a_validators
from auths.models import Category
from helpers.models import TimestampMixin
from .base import User


class Statement(TimestampMixin, models.Model):
    """
    Модель заявки.
    """
    categories = models.ManyToManyField(
        Category,
        through='StatementCategory',
        related_name='statement_categories',
        verbose_name='Категория'
    )
    author = models.ForeignKey(
        User,
        #on_delete=models.SET_NULL,
        on_delete=models.CASCADE,
        verbose_name='Составитель заявки',
        null=True, blank=True
    )
    text = models.TextField(
        'Сообщение'
    )
    service_time = models.DateTimeField(
        'дата предоставление услуги',
        null=True
    )
    location = models.TextField(
        'Место встречи',
        null=True
    )
    min_price = models.PositiveBigIntegerField(
        'Минимальная цена',
    )
    max_price = models.PositiveBigIntegerField(
        'Максимальная цена',
    )
    is_active = models.BooleanField(
        'Статус',
        default=True
    )
    is_busy_by_provider = models.BooleanField(
        'Статус в работе провайдером или сделано',
        default=False,
    )
    created_at = models.DateTimeField(
        'дата создания заявки',
        auto_now_add=True,
        null=True
    )

    class Meta:
        verbose_name = 'заказ собственника'
        verbose_name_plural = 'заказы собственников'

    def is_seen_by(self, user):
        if user.is_provider:
            return SeenStatement.objects.filter(user=user, statement=self).exists()
        return False

    def mark_as_seen(self, user):
        if user.is_provider:
            SeenStatement.objects.get_or_create(user=user, statement=self)


class StatementMedia(models.Model):
    statement = models.ForeignKey(
        Statement,
        related_name='media',
        verbose_name='Фотографии/Видео сооружения',
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        upload_to='statement_media/',
        validators=[a_validators.validate_files_extension],
        null=True,
        blank=True,
    )
    file_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')], blank=True)

    class Meta:
        verbose_name = 'медиафайл заявки собственника'
        verbose_name_plural = 'медиафайлы заявки собственников'

    def save(self, *args, **kwargs):
        if self.file:
            extension = self.file.name.split('.')[-1].lower()
            if extension in ['jpg', 'jpeg', 'png']:
                self.file_type = 'image'
            elif extension in ['mp4', 'mov', 'avi']:
                self.file_type = 'video'
        super().save(*args, **kwargs)


class SeenStatement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    statement = models.ForeignKey('Statement', on_delete=models.CASCADE)
    seen_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'statement')
