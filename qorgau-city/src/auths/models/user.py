import auths
import auths.validators as a_validators
from auths import INSPECTOR_RANK, INSPECTOR_POSITION, ORGANIZATION_MAIN_TYPE, ORGANIZATION_TYPE
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from helpers.models import CustomType
from storages.backends.s3boto3 import S3Boto3Storage

from .category import Category
from .manager import CustomUserManager
from .role import CustomUserRole


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model extending AbstractBaseUser and PermissionsMixin.
    """

    class Status(models.TextChoices):
        ACCEPTED = 'ACCEPTED', 'Принято'
        NOT_ACCEPTED = 'NOT_ACCEPTED', 'Не принято'

    last_name = models.CharField(
        max_length=255,
        verbose_name='фамилия',
        blank=True,
        null=True,
        validators=[
            a_validators.validate_alpha,
        ]
    )
    first_name = models.CharField(
        max_length=255,
        verbose_name='имя',
        blank=True,
        null=True,
        validators=[
            a_validators.validate_alpha,
        ]
    )
    middle_name = models.CharField(
        max_length=255,
        verbose_name='отчество',
        blank=True,
        null=True,
        validators=[
            a_validators.validate_alpha,
        ]
    )
    phone_regex = RegexValidator(
        regex=r'^\+?[0-9]{1,12}$',
        message='Номер телефона должен вводиться в формате: +77123456789'
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=12,
        verbose_name='номер телефона',
        unique=True,
        blank=True
    )
    email = models.EmailField(
        unique=True,
        verbose_name='почта'
    )
    birthdate = models.DateField(
        verbose_name='Дата рождения',
        blank=True,
        null=True,
    )
    role = models.ManyToManyField(
        CustomUserRole,
        through="UserRole",
        through_fields=('user', 'role'),
        verbose_name="роль",
        related_name="users",
        blank=True,
    )
    avatar_url = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[a_validators.validate_file_extension],
        storage=S3Boto3Storage(location='avatars/')
    )
    is_superuser = models.BooleanField(
        verbose_name='superuser',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name='active',
        default=False
    )
    is_staff = models.BooleanField(
        verbose_name='staff',
        default=False
    )
    iin = models.CharField(
        max_length=12,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{12}$',
                message="IIN must be exactly 12 digits."
            )
        ],
        verbose_name="иин"
    )
    actual_residence_address = models.CharField(
        max_length=255,
        verbose_name='Адрес фактического проживания гражданина',
        null=True,
        blank=True,
    )
    residence_address = models.CharField(
        max_length=255,
        verbose_name='Адрес прописки гражданина',
        null=True,
        blank=True,
    )

    bin_field = models.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{12}$',
                message="BIN must be exactly 12 digits."
            )
        ],
        verbose_name="бин",
        null=True,
        blank=True,
    )

    rank = models.CharField(
        'Звание',
        max_length=50,
        choices=INSPECTOR_RANK.choices,
        default=INSPECTOR_RANK.Private_Civil_Protection,
    )
    position = models.CharField(
        'Должность',
        max_length=50,
        choices=INSPECTOR_POSITION.choices,
        default=INSPECTOR_POSITION.Chief_State_Inspector_for_Fire_Control,
    )
    certificate_number = models.CharField(
        'Номер удостоверения',
        blank=True,
        null=True,
    )
    inspector_jurisdiction_city = models.CharField(
        max_length=255,
        verbose_name='Город юрисдикции инспектора',
        null=True,
        blank=True,
    )
    inspector_jurisdiction_district = models.CharField(
        max_length=255,
        verbose_name='Район юрисдикции инспектора',
        null=True,
        blank=True,
    )

    about_myself = models.TextField(
        verbose_name='О себе',
        max_length=255,
        blank=True,
        null=True,
    )
    main_organization_type = models.CharField(
        "Главный тип организации(Коммерческое или НеКоммерческое)",
        max_length=50,
        choices=ORGANIZATION_MAIN_TYPE.choices,
        default=ORGANIZATION_MAIN_TYPE.Commercial_Organizations,
    )
    organization_type = models.CharField(
        'Тип организации',
        max_length=200,
        choices=ORGANIZATION_TYPE.choices,
        default=ORGANIZATION_TYPE.State_Owned_Enterprises,
    )
    organization_sub_type = models.CharField(
        'ПодТип Организации',
        max_length=200,
        blank=True,
        null=True,
    )
    organization_name = models.TextField(
        'Наименование организации',
        blank=True, null=True
    )
    company_name = models.TextField(
        'Название компании',
        blank=True, null=True
    )
    categories = models.ManyToManyField(
        Category,
        through='UserCategory',
        related_name='users',
        verbose_name='Категории'
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ('-id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    @property
    def get_fullname(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def get_user_roles(self):
        """
        Returns the user's roles as a list of strings.
        """
        if self.is_superuser:
            return 'superuser'
        user_roles = [self.role.all()[i].role for i in range(len(self.role.all()))]
        return user_roles

    @property
    def is_inspector(self):
        """
        Checks if the user has the role of 'INSPECTOR'.
        """
        return self.role.all().filter(role='INSPECTOR').exists()

    @property
    def is_provider(self):
        """
        Checks if the user has the role of 'PROVIDER'.
        """
        return self.role.all().filter(role='PROVIDER').exists()

    @property
    def is_object_owner(self):
        """
        Checks if the user has the role of 'OBJECT_OWNER'.
        """
        return self.role.all().filter(role='OBJECT_OWNER').exists()

    @property
    def is_citizen(self):
        """
        Checks if the user has the role of 'CITIZEN'.
        """
        return (self.role.all().filter(role='CITIZEN').exists())

    @property
    def has_single_role(self):
        return (self.role.count() < 2)

    @property
    def provider_categories(self):
        return Category.objects.filter(
            user_categories__user=self,
            user_categories__role='PROVIDER'
        )

    # @property
    # def object_owner_categories(self):
    #     return Category.objects.filter(
    #         user_categories__user=self,
    #         user_categories__role='OBJECT_OWNER'
    #     )


class UserCategory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='user_categories')
    role = models.CharField(
        max_length=50,
        choices=auths.UserCategoryType.choices,
        default=auths.UserCategoryType.PROVIDER,
    )

    class Meta:
        unique_together = ['user', 'category', 'role']
        verbose_name = 'User Category'
        verbose_name_plural = 'User Categories'

    def __str__(self):
        return f"{self.user.get_fullname} - {self.category.name} ({self.role})"

    def clean(self):
        if self.role == 'PROVIDER' and not self.user.is_provider:
            raise ValidationError("User must have a Provider role to be associated with a provider category.")
        # if self.role == 'OBJECT_OWNER' and not self.user.is_object_owner:
        #     raise ValidationError("User must have an Object Owner role to be associated with an object owner category.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
