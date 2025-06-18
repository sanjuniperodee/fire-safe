#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from objects.models import Document, DocumentKey, Building
from auths.models import CustomUser

print("=== Проверка документов ===")
total_docs = Document.objects.count()
main_docs = Document.objects.filter(parent__isnull=True).count()
child_docs = Document.objects.filter(parent__isnull=False).count()

print(f"Всего документов: {total_docs}")
print(f"Главных документов: {main_docs}")
print(f"Дочерних документов: {child_docs}")
print(f"Ключей документов: {DocumentKey.objects.count()}")

print("\nПервые 5 главных документов:")
for doc in Document.objects.filter(parent__isnull=True)[:5]:
    print(f"- {doc.title}")
    child_count = Document.objects.filter(parent=doc).count()
    if child_count > 0:
        print(f"  Дочерних: {child_count}")

print("\nПроверим, есть ли документ III главы:")
third_chapter = Document.objects.filter(
    title="III. Архитектурно-строительная часть – требования пожарной безопасности к зданиям и сооружениям"
).first()
if third_chapter:
    print("III глава найдена!")
    children = Document.objects.filter(parent=third_chapter)
    print(f"У неё дочерних документов: {children.count()}")
    for child in children:
        print(f"  - {child.title}")
else:
    print("III глава НЕ найдена!") 