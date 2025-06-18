from django.db import models
from django.core.exceptions import ValidationError

from auths.models import CustomUser
from objects.models import Building, DocumentKey

from helpers.models import TimestampMixin


class BuildingRemark(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Объект'
    )
    inspector = models.ForeignKey(
        CustomUser,
        # on_delete=models.SET_NULL,
        on_delete=models.CASCADE,
        null=True,
        related_name='building_notes',
        verbose_name='Инспектор'
    )
    content = models.TextField(
        verbose_name='Содержание примечания'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    # updated_at = models.DateTimeField(
    #     auto_now=True,
    #     verbose_name='Дата обновления'
    # )

    class Meta:
        verbose_name = 'Примечание к объекту'
        verbose_name_plural = 'Примечания к объектам'
        ordering = ['-created_at']

    def __str__(self):
        return f"Примечание для здания {self.building} от {self.inspector}"

    def clean(self):
        if not self.inspector.is_inspector:
            raise ValidationError("Только инспекторы могут создавать примечания к объектам.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class DocumentRemark(TimestampMixin, models.Model):
    # document_key_file = models.ForeignKey(
    #     'DocumentKeyFile',
    #     on_delete=models.CASCADE,
    #     related_name='remarks',
    #     verbose_name='документ'
    # )
    document_key = models.ForeignKey(
        DocumentKey,
        on_delete=models.CASCADE,
        related_name='remarks',
        verbose_name='документ'
    )
    # document_key = models.ForeignKey(
    #     DocumentKey,
    #     on_delete=models.CASCADE,
    #     related_name='comment',
    #     verbose_name='документ'
    # )
    # inspector = models.ForeignKey(
    #     CustomUser,
    #     on_delete=models.CASCADE,
    #     related_name='document_remarks',
    #     verbose_name='инспектор'
    # )
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        related_name='remarks',
        null=True, blank=True
    )
    content = models.TextField('содержание примечания')
    created_at = models.DateTimeField(
        'дата создания заявки',
        auto_now_add=True,
        null=True
    )

    # is_resolved = models.BooleanField('разрешено', default=False)
    # resolved_at = models.DateTimeField('дата разрешения', null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Примечание к документу'
        verbose_name_plural = 'Примечания к документам'

    def __str__(self):
        # return f'Примечание к документу {self.document_key} от инспектора {self.inspector}'
        return f'Примечание к документу {self.document_key} от инспектора'

    # def resolve(self):
    #     from django.utils import timezone
    #     self.is_resolved = True
    #     self.resolved_at = timezone.now()
    #     self.save()
