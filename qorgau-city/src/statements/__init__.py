from django.db.models import TextChoices


class StatementStatus(TextChoices):
    OPENED = 'OPENED', 'Открыто'
    IN_WORK = 'IN_WORK', 'В работе'
    COMPLETED = 'COMPLETED', 'Выполнено'
    ARCHIVED = 'ARCHIVED', 'В архиве'