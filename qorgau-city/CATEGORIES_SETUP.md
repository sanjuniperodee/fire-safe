# Настройка категорий услуг

## Проблема
При создании заявок (statements) возникает ошибка:
```
{"categories":["Недопустимый первичный ключ \"1\" - объект не существует."]}
```

Это происходит потому, что в базе данных отсутствуют категории услуг, которые используются на фронтенде.

## Решение

### 1. Исправление nginx.conf (уже исправлено)
В файле `qorgau-city-front/nginx.conf` была исправлена ошибка в строке 17:
```diff
- gzip_proxied expired no-cache no-store private must-revalidate auth;
+ gzip_proxied expired no-cache no-store private auth;
```

### 2. Инициализация категорий в базе данных

#### Вариант A: Использование отдельной команды
```bash
# На сервере, в папке с проектом
cd ~/fire-safe/qorgau-city
docker-compose exec app_backend python manage.py init_categories
```

#### Вариант B: Полная переинициализация проекта
```bash
# На сервере, в папке с проектом
cd ~/fire-safe/qorgau-city
docker-compose exec app_backend python manage.py init_project
```

### 3. Пересборка и перезапуск frontend контейнера
```bash
# Пересобираем frontend с исправленным nginx.conf
docker-compose build frontend

# Перезапускаем контейнеры
docker-compose up -d
```

### 4. Проверка
После выполнения команд проверьте:
1. Логи frontend контейнера: `docker-compose logs frontend`
2. Доступность сайта: `http://165.22.63.97:5173`
3. Создание заявки должно работать без ошибок

## Список категорий
В системе будут созданы 39 категорий услуг:
1. Определение качества огнезащитной обработки деревянных конструкций
2. Определение качества огнезащитной обработки стальных конструкций
3. Определение прочности пожарных лестниц
4. Текстильные материалы и ткани
5. Пенообразователи
6. Герметизирующие материалы
7. Вентиляционные системы
8. Обучение персонала
9. Монтаж систем безопасности
10. И другие...

## Техническая информация

### Файлы, которые были изменены:
- `qorgau-city-front/nginx.conf` - исправлена ошибка gzip_proxied
- `qorgau-city/src/auths/management/commands/init_categories.py` - новая команда
- `qorgau-city/src/auths/management/commands/init_project.py` - обновлена для включения категорий

### Модель Category:
```python
class Category(models.Model):
    name = models.TextField('Категория', blank=False, null=False)
    measurement_unit = models.CharField('Единица измерения', max_length=255, blank=True, null=True)
```

Категории берутся из файла `qorgau-city-front/src/utils/categoryList.ts` и синхронизируются с базой данных. 