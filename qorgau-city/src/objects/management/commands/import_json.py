import json
from pathlib import Path

from django.core.management.base import BaseCommand

from auths.models import Category

files = {'categories': Category}


class Command(BaseCommand):
    help = 'Import data from JSON file'

    def handle(self, *args, **kwargs):
        for file in files:
            file_path = f'objects/management/commands/files/{file}.json'
            if not Path(file_path).is_file():
                print(f'Файл {file}.json не найден.')
                return
            with open(file_path, encoding='utf-8') as fh:
                data = json.load(fh)

            model = files[file]
            for item in data:
                if not model.objects.filter(**item).exists():
                    new_item = model(**item)
                    new_item.save()

            print(f'Файл {file}.json успешно загружен.')
