from django.db import models
# from storages.backends.s3boto3 import S3Boto3Storage

from helpers.models import TimestampMixin
from helpers.utils import delete_file

class OrganizationType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Тип организации"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип организации'
        verbose_name_plural = 'Типы организаций'


class Document(
    TimestampMixin,
    models.Model
):
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='childs',
        null=True,
        blank=True,
        #verbose_name='Глава документа',
    )
    title = models.CharField(
        'название',
        max_length=255,
        unique=True
    )

    class Meta:
        verbose_name = 'Глава документа'
        verbose_name_plural = 'Главы документов'

    def __str__(self):
        return self.title


class DocumentKey(
    TimestampMixin,
    models.Model
):
    title = models.TextField('название')
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='keys'
    )

    supported_organization_types = models.ManyToManyField(
        OrganizationType,
        related_name='document_types',
        verbose_name='Поддерживаемые типы зданий'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return f'{self.document.title[:20]}...: {self.title[:30]}...'


class DocumentKeyFile(
    TimestampMixin,
    models.Model
):
    name = models.CharField(
        'название',
        max_length=255,
        null=True,
        blank=True
    )
    path = models.FileField(
        'путь',
        max_length=255,
        null=True,
        blank=True,
        upload_to="private/%Y/%m/",
    )
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='объект'
    )
    document_key = models.ForeignKey(
        DocumentKey,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='документ'
    )

    def delete(self, using=None, keep_parents=False):
        delete_file(self.path)
        super().delete(using=using, keep_parents=keep_parents)

    class Meta:
        ordering = ('id',)
        verbose_name = 'Файл'
        verbose_name_plural = 'Загруженные файлы'

    def __str__(self):
        return f'{self.path}'


class DocumentComment(
    TimestampMixin,
    models.Model
):
    body = models.TextField(
        'название'
    )
    document_key = models.ForeignKey(
        DocumentKey,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='документ'
    )
    building = models.ForeignKey(
        'Building',
        on_delete=models.CASCADE,
        related_name='comment',
        null=True, blank=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Комментарий к документу'
        verbose_name_plural = 'Комментарии к документам'
