from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
import auths

User = get_user_model()


class Command(BaseCommand):
    help = 'Create users'

    def handle(self, *args, **kwargs):
        User.objects.create(
            phone='+77012345678',
            password=make_password('Simple12'),
            is_superuser=False,
            is_active=True,
            is_staff=False,
            last_name='Собственник',
            first_name='Влад',
            middle_name='Вович',
            iin='000101222222',
            email='owner1@example.ru',
            birthdate='2020-02-02',
            status=auths.Status.ACCEPTED,
            role=auths.Role.OBJECT_OWNER
        )
        User.objects.create(
            phone='+77023456789',
            password=make_password('Simple12'),
            is_superuser=False,
            is_active=True,
            is_staff=False,
            last_name='Тожесобственник',
            first_name='Грег',
            middle_name='Вович',
            iin='000101333333',
            email='owner2@example.ru',
            birthdate='2020-03-03',
            status=auths.Status.ACCEPTED,
            role=auths.Role.OBJECT_OWNER
        )
        User.objects.create(
            phone='+77034567890',
            password=make_password('Simple12'),
            is_superuser=False,
            is_active=True,
            is_staff=False,
            last_name='Инспектор',
            first_name='Первый',
            middle_name='Аович',
            iin='000101444444',
            email='inspector1@example.ru',
            birthdate='2020-04-04',
            status=auths.Status.ACCEPTED,
            role=auths.Role.INSPECTOR
        )
        User.objects.create(
            phone='+77045678901',
            password=make_password('Simple12'),
            is_superuser=False,
            is_active=True,
            is_staff=False,
            last_name='Ещенспектор',
            first_name='Второй',
            middle_name='Аович',
            iin='000101777777',
            email='inspector2@example.ru',
            birthdate='2020-05-05',
            status=auths.Status.ACCEPTED,
            role=auths.Role.INSPECTOR
        )

        print('Пользователи успешно загружены.')
