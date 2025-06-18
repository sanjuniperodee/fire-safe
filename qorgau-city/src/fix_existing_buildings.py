#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from objects.models import Document, Building

def attach_all_documents_to_building(building):
    """
    Привязывает все документы к объекту
    """
    all_documents = Document.objects.all()
    building.documents.set(all_documents)
    print(f"К объекту {building.id} привязано {all_documents.count()} документов")

print("=== Привязка документов к существующим объектам ===")

# Получаем все объекты
buildings = Building.objects.all()
print(f"Найдено объектов: {buildings.count()}")

for building in buildings:
    current_docs = building.documents.count()
    print(f"\nОбъект ID {building.id}: {building.address}")
    print(f"  Сейчас привязано: {current_docs} документов")
    
    if current_docs == 0:
        print("  Привязываем все документы...")
        attach_all_documents_to_building(building)
    else:
        print("  Документы уже привязаны")

print("\n=== Результат ===")
for building in Building.objects.all():
    docs_count = building.documents.count()
    print(f"Объект ID {building.id}: {docs_count} документов") 