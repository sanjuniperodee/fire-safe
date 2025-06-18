from django.db import models

from statements import StatementStatus
from helpers.models import TimestampMixin
from .base import User
import auths


class StatementProvider(TimestampMixin):
    statement = models.ForeignKey(
        'Statement',
        on_delete=models.CASCADE,
        related_name='provider_responses',
        verbose_name='Заявка'
    )
    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='responded_statements',
        verbose_name='Поставщик',
        limit_choices_to={'role__role': auths.Role.PROVIDER}
    )
    chat_room_id = models.IntegerField(
        verbose_name='ID комнаты чата провайдера и собственника',
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=StatementStatus.choices,
        default=StatementStatus.OPENED,
        verbose_name='статус заявки',
    )
    archive_date = models.DateTimeField(
        verbose_name='дата архива заявки(истек срок)',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Отклик поставщика'
        verbose_name_plural = 'Отклики поставщиков'
        unique_together = ['statement', 'provider']
        ordering = ['-created_at']

    def __str__(self):
        return f"Отклик на заявку {self.statement.id} от {self.provider.get_fullname}"

    def save(self, *args, **kwargs):
        if not self.provider.is_provider:
            raise ValueError("User must have a Provider role to respond to a statement.")
        super().save(*args, **kwargs)


class StatementRequestForCompleted(TimestampMixin):
    statement = models.ForeignKey(
        'Statement',
        on_delete=models.CASCADE,
        verbose_name='Заявка'
    )
    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Поставщик',
    )
    is_completed = models.BooleanField(
        'Статус запроса на выполнено',
        default=False,
    )

    class Meta:
        verbose_name = 'Запрос заказа на Выполнено от Провайдера'
        verbose_name_plural = 'Запросы заказов на Выполнено от Провайдеров'