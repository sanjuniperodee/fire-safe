import auths
from django.db import models


class CustomUserRole(models.Model):
    """
    Model representing roles available for CustomUser instances.
    """

    role = models.CharField(
        max_length=100,
        verbose_name="роль",
        choices=auths.Role.choices
    )

    def __str__(self):
        return self.role

    @property
    def can_add_provider(self):
        return (self.role in auths.ALLOWED_ROLES['provider'])

    @property
    def can_add_object_owner(self):
        return (self.role in auths.ALLOWED_ROLES['object_owner'])

    @property
    def can_add_citizen(self):
        return (self.role == auths.Role.CITIZEN)

    class Meta:
        ordering = ('-id',)


class UserRole(models.Model):
    """
    Model representing the role assigned to a user.
    """
    user = models.ForeignKey(
        "CustomUser",
        on_delete=models.CASCADE,
        related_name='user_roles'
    )
    role = models.ForeignKey(
        CustomUserRole,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=auths.Status.choices,
        default=auths.Status.NOT_ACCEPTED,
        help_text='Гражданин не имеет статуса',
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "role_user_roles"
        verbose_name = 'роли пользователей'
        verbose_name_plural = 'Роли пользователей'

    def __str__(self):
        return f"{self.role.role} - {self.status}"
