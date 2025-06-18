import json
from django.core.management.base import BaseCommand

from objects.models import Document, DocumentKey
import auths
from auths.models import CustomUser, CustomUserRole, UserRole
from helpers.logger import log_exception
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Create documents and info'

    def handle(self, *args, **kwargs):
        try:
            print('Starting create documents and info...')
            print("1" * 10)

            with open('objects/management/commands/files/documents.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
            print("1" * 10)

            admin_role = None
            for role in auths.Role.choices:
                new_role = CustomUserRole.objects.get_or_create(role=role[0])
                admin_role = new_role if role[0] == 'INSPECTOR' else admin_role

            admin = CustomUser.objects.create(
                phone='+77777777777',
                password=make_password('qor321gau'),  # 123
                is_superuser=True,
                is_active=True,
                is_staff=True,
                first_name='admin',
                email='admin@example.com',
                iin="000101555555"
            )

            # Поставить роль АДМИН
            # user_role = UserRole(user=admin, role=admin_role[0], status=auths.Status.ACCEPTED)
            # user_role.save()

            print("1" * 10)
            for item in data['info']:
                title = item.get('title', None)
                sub_paragraphs = item.get('subParagraphs', None)
                keys = item.get('keys', [])
                print("2" * 10)
                if title:
                    print(f"Processing {title}...")
                    document = Document.objects.create(title=title)
                    if sub_paragraphs:
                        for sub_item in sub_paragraphs:
                            sub_title = sub_item.get('title', None)
                            sub_keys = sub_item.get('keys', [])

                            if sub_title:
                                print(f"Processing {sub_title}...")
                                sub_document = Document.objects.create(title=sub_title, parent=document)
                                for sub_key in sub_keys:
                                    DocumentKey.objects.create(
                                        title=sub_key.get('title'),
                                        document=sub_document
                                    )
                    print("3" * 10)
                    for key in keys:
                        DocumentKey.objects.create(title=key.get('title'), document=document)
                    print("4" * 10)

        except Exception as e:
            print(e)
            log_exception(e)
            return
