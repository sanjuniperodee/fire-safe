#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from objects.models import Document, DocumentKey, Building

print("=== Исправление привязки ключей документов ===")

# Получаем все объекты
buildings = Building.objects.all()
all_document_keys = DocumentKey.objects.all()

print(f"Найдено объектов: {buildings.count()}")
print(f"Всего ключей документов: {all_document_keys.count()}")

for building in buildings:
    current_keys = building.document_keys.count()
    print(f"\nОбъект ID {building.id}: {building.address}")
    print(f"  Сейчас привязано ключей: {current_keys}")
    
    if current_keys < all_document_keys.count():
        print("  Привязываем все ключи документов...")
        building.document_keys.set(all_document_keys)
        print(f"  Привязано {all_document_keys.count()} ключей")
    else:
        print("  Ключи уже привязаны")

print("\n=== Результат ===")
for building in Building.objects.all():
    docs_count = building.documents.count()
    keys_count = building.document_keys.count()
    print(f"Объект ID {building.id}: {docs_count} документов, {keys_count} ключей") 