#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from objects.models import Document, DocumentKey, Building

print("=== Детальная проверка структуры документов ===")

# Проверим структуру III главы
third_chapter = Document.objects.filter(
    title="III. Архитектурно-строительная часть – требования пожарной безопасности к зданиям и сооружениям"
).first()

if third_chapter:
    print(f"III глава найдена: {third_chapter.title}")
    children = Document.objects.filter(parent=third_chapter)
    print(f"Дочерних документов: {children.count()}")
    
    if children.exists():
        print("Дочерние документы:")
        for child in children:
            print(f"  - {child.title}")
    else:
        print("ПРОБЛЕМА: У III главы нет дочерних документов!")
else:
    print("III глава не найдена!")

print("\n=== Проверим все главы ===")
for i in range(1, 15):  # 14 глав
    if i <= 9:
        roman = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'][i-1]
    else:
        roman = ['X', 'XI', 'XII', 'XIII', 'XIV'][i-10]
    
    chapter = Document.objects.filter(title__startswith=f"{roman}.").first()
    if chapter:
        children_count = Document.objects.filter(parent=chapter).count()
        print(f"{roman} глава: {children_count} дочерних документов")
    else:
        print(f"{roman} глава: НЕ НАЙДЕНА")

# Проверим последний объект
print("\n=== Последний созданный объект ===")
last_building = Building.objects.last()
if last_building:
    print(f"Объект ID {last_building.id}: {last_building.documents.count()} документов")
    print(f"Рейтинг: {last_building.rating}")
    
    # Посчитаем вручную
    total_docs = Document.objects.count()
    print(f"Всего документов в системе: {total_docs}")
    
    # Проверим calculation_building_rating
    from helpers.calculation_building_rating import calculation_building_rating
    try:
        rating = calculation_building_rating(last_building.id)
        print(f"Рейтинг через функцию: {rating}")
    except Exception as e:
        print(f"Ошибка при расчете рейтинга: {e}")
else:
    print("Объектов нет") 