from django.db import models

from statements import StatementStatus
from helpers.models import TimestampMixin
from .base import User
import auths


class StatementSuggestion(TimestampMixin):
    """
    Model to store suggestions/counter-offers from statement authors to providers.
    """
    statement = models.ForeignKey(
        'Statement',
        on_delete=models.CASCADE,
        related_name='author_suggestions',
        verbose_name='Заявка'
    )
    provider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_suggestions',
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
        verbose_name = 'Предложение автора заявки к провайдеру'
        verbose_name_plural = 'Предложения авторов заявок к провайдерам'
        # unique_together = ['statement', 'provider']
        ordering = ['-created_at']

    def __str__(self):
        return f"Предложение по заявке {self.statement.id} для {self.provider.get_fullname}"

    def save(self, *args, **kwargs):
        if not self.provider.is_provider:
            raise ValueError("User must have a Provider role to receive suggestions.")
        super().save(*args, **kwargs)