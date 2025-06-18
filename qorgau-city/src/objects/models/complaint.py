import uuid
from datetime import timedelta
from datetime import timezone

from django.db import models
from django.db.models import Subquery, OuterRef
from django.utils import timezone

import auths
from auths.models import CustomUser
from auths.models import UserRole
from objects import Status
from helpers.models import TimestampMixin


class Complaint(TimestampMixin, models.Model):
    """
    Сделать заявление/жалобу интегрированная с Chat API
    Сообщить о пожаре
    """

    unique_id = models.UUIDField(
    default=uuid.uuid4,
    editable=False,
    unique=True,
    blank=False,   # обязательно False
    null=False     # обязательно False
)
    author = models.ForeignKey(
        CustomUser, verbose_name='заявитель',
        # on_delete=models.SET_NULL,
        on_delete=models.CASCADE,
        null=True,
        related_name='authored_complaints',
    )
    inspector = models.ForeignKey(
        CustomUser, verbose_name='инспектор',
        # on_delete=models.SET_NULL,
        on_delete=models.CASCADE,
        null=True,
        related_name='assigned_complaints',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='статус жалобы',
    )
    expiration_date = models.DateTimeField(
        verbose_name='дата истечения срока жалобы(не отвечен)',
        blank=True,
        null=True,
    )
    archive_date = models.DateTimeField(
        verbose_name='дата архива жалобы(истек срок)',
        blank=True,
        null=True,
    )
    chat_room_id = models.IntegerField(
        verbose_name='ID комнаты чата гражданина и инспектора',
        null=True,
        blank=True,
    )
    # building address
    city = models.CharField(
        max_length=100,
        null=True,
        verbose_name='город расположения здания(отправить жалобу)'
    )
    district = models.CharField(
        max_length=100,
        null=True,
        verbose_name='район расположения здания(отправить жалобу)',
    )
    address_detail = models.TextField(
        null=True,
        verbose_name='подробный адрес(отправить жалобу)',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'жалоба от гражданина'
        verbose_name_plural = 'Жалобы от гражданина'

    def __str__(self):
        return (f'Complaint {self.unique_id} by {self.author} to '
                f'building {self.city}{self.district}{self.address_detail}')

    # def save(self, *args, **kwargs):
    #     if not self.expiration_date:
    #         self.expiration_date = timezone.now() + timedelta(days=14)
    def save(self, *args, **kwargs):
        print("Saving complaint:", self.unique_id)
        if not self.expiration_date:
            # timedelta(minutes=1)
            # self.expiration_date = timezone.now() + timedelta(days=14)
            self.expiration_date = timezone.now() + timedelta(minutes=10)
            # self.archive_date = timezone.now() + timedelta(days=30)
            self.archive_date = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)
        print("Complaint saved successfully")

    @classmethod
    def assign_inspector(cls, city, district, status=auths.Status.ACCEPTED):
        # Subquery to get the status of the INSPECTOR role for each user
        inspector_status_subquery = UserRole.objects.filter(
            user=OuterRef('pk'),
            role__role=auths.Role.INSPECTOR
        ).values('status')[:1]

        inspectors = CustomUser.objects.filter(
            role__role=auths.Role.INSPECTOR,
            inspector_jurisdiction_city=city,
            inspector_jurisdiction_district=district,
            is_active=True
        ).annotate(
            inspector_status=Subquery(inspector_status_subquery)
        ).filter(
            inspector_status=status
        )
        # print(f'inspectors: {inspectors}')
        if inspectors.exists():
            least_assigned_inspector = min(inspectors, key=lambda i: i.assigned_complaints.count())
            # print(f'least_assigned_inspector: {least_assigned_inspector}')
            return least_assigned_inspector
        return None

    @classmethod
    def update_expired_complaints(cls):
        expired_complaints = cls.objects.filter(
            expiration_date__lte=timezone.now(),
            status=cls.Status.PENDING,
        )
        expired_complaints.update(status=cls.Status.EXPIRED)

    def mark_as_answered(self):
        self.status = Status.ANSWERED
        self.save()

    def mark_as_not_answered(self):
        if self.status == Status.PENDING and timezone.now() >= self.expiration_date:
            self.status = Status.NOT_ANSWERED
            self.save()

    def mark_as_expired(self):
        if self.status == Status.ANSWERED and timezone.now() >= self.archive_date:
            self.status = Status.EXPIRED
            self.save()
