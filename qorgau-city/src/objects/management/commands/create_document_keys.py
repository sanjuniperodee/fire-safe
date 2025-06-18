# objects/management/commands/create_document_keys.py

from django.core.management.base import BaseCommand, CommandError
from objects.models.document import Document, DocumentKey, OrganizationType

class Command(BaseCommand):
    help = 'Создаёт DocumentKey с указанными названиями и присваивает им supported_organization_types с заданным ID'

    def add_arguments(self, parser):
        parser.add_argument(
            '--document_id',
            type=int,
            required=True,
            help='ID существующего Document для связывания с DocumentKeys'
        )
        parser.add_argument(
            '--organization_type_id',
            type=int,
            default=2,
            help='ID OrganizationType для присвоения DocumentKeys'
        )
        parser.add_argument(
            '--titles_file',
            type=str,
            required=True,
            help='Путь к текстовому файлу с названиями DocumentKey, по одному названию на строку'
        )

    def handle(self, *args, **options):
        document_id = options['document_id']
        org_type_id = options['organization_type_id']
        titles_file = options['titles_file']

        # Получаем Document
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            raise CommandError(f"Document с ID {document_id} не существует.")

        # Получаем OrganizationType
        try:
            org_type = OrganizationType.objects.get(id=org_type_id)
        except OrganizationType.DoesNotExist:
            raise CommandError(f"OrganizationType с ID {org_type_id} не существует.")

        # Читаем названия из файла
        try:
            with open(titles_file, 'r', encoding='utf-8') as f:
                titles = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            raise CommandError(f"Файл с названиями '{titles_file}' не найден.")

        if not titles:
            self.stdout.write(self.style.WARNING('Файл с названиями пуст.'))
            return

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for title in titles:
            doc_key, created = DocumentKey.objects.get_or_create(
                title=title,
                document=document  # Указываем и документ
            )
            if created:
                doc_key.supported_organization_types.add(org_type)
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Создан DocumentKey: {title}"))
            else:
                # Если DocumentKey уже существует, проверяем, добавлен ли org_type
                if not doc_key.supported_organization_types.filter(id=org_type_id).exists():
                    doc_key.supported_organization_types.add(org_type)
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Обновлен DocumentKey: {title} с OrganizationType ID={org_type_id}"))
                else:
                    skipped_count += 1
                    self.stdout.write(self.style.WARNING(f"DocumentKey уже существует и имеет OrganizationType ID={org_type_id}: {title}"))

        self.stdout.write(self.style.SUCCESS(f"Итого: {created_count} создано, {updated_count} обновлено, {skipped_count} пропущено."))
