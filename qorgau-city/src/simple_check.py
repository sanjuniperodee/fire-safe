#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from objects.models import Document, DocumentKey, Building

print("=== Структура документов ===")

# Проверим все главы 
main_documents = Document.objects.filter(parent__isnull=True).order_by('title')
print(f"Главных документов: {main_documents.count()}")

for doc in main_documents:
    children = Document.objects.filter(parent=doc)
    keys = DocumentKey.objects.filter(document=doc)
    print(f"\n{doc.title}")
    print(f"  Дочерних документов: {children.count()}")
    print(f"  Ключей: {keys.count()}")
    
    if children.exists():
        for child in children:
            child_keys = DocumentKey.objects.filter(document=child)
            print(f"    - {child.title} (ключей: {child_keys.count()})")

print(f"\n=== Итого ===")
print(f"Всего документов: {Document.objects.count()}")
print(f"Всего ключей: {DocumentKey.objects.count()}")

# Проверим последний объект
last_building = Building.objects.last()
if last_building:
    print(f"\nПоследний объект ID {last_building.id}:")
    print(f"  Привязано документов: {last_building.documents.count()}")
    print(f"  Рейтинг: {last_building.rating}") 