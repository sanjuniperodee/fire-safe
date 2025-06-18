# 🔥 Fire Safety Management System (Qorgau City)

Система управления пожарной безопасностью для городов Казахстана.

## 🚀 Быстрый запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/sanjuniperodee/fire-safe.git
cd fire-safe
```

### 2. Запуск через Docker Compose
```bash
# Запуск всех сервисов
docker-compose up -d

# Проверка статуса
docker-compose ps
```

### 3. Инициализация проекта (ВАЖНО!)
После запуска контейнеров выполните команду для создания всех ролей, инспекторов и администратора:

```bash
# Войти в контейнер Django
docker-compose exec web bash

# Выполнить миграции
python manage.py migrate

# Инициализировать проект (создать роли, инспекторов, админа)
python manage.py init_project
```

## 👥 Учетные данные по умолчанию

### 👤 Администратор
- **Телефон:** `+77758489538`
- **Пароль:** `u4DwQw04`
- **Email:** `admin@qorgau.kz`

### 👨‍💼 Инспекторы по городам
Система автоматически создает инспекторов для всех крупных городов Казахстана:

| Город | Телефон | Пароль | Email |
|-------|---------|--------|-------|
| Алматы | +77758481001 | inspector01 | inspector.алматы@qorgau.kz |
| Нур-Султан | +77758481002 | inspector02 | inspector.нур-султан@qorgau.kz |
| Шымкент | +77758481003 | inspector03 | inspector.шымкент@qorgau.kz |
| Актобе | +77758481004 | inspector04 | inspector.актобе@qorgau.kz |
| Тараз | +77758481005 | inspector05 | inspector.тараз@qorgau.kz |
| Павлодар | +77758481006 | inspector06 | inspector.павлодар@qorgau.kz |
| Усть-Каменогорск | +77758481007 | inspector07 | inspector.усть-каменогорск@qorgau.kz |
| Семей | +77758481008 | inspector08 | inspector.семей@qorgau.kz |
| Атырау | +77758481009 | inspector09 | inspector.атырау@qorgau.kz |
| Костанай | +77758481010 | inspector10 | inspector.костанай@qorgau.kz |
| Кызылорда | +77758481011 | inspector11 | inspector.кызылорда@qorgau.kz |
| Уральск | +77758481012 | inspector12 | inspector.уральск@qorgau.kz |
| Петропавловск | +77758481013 | inspector13 | inspector.петропавловск@qorgau.kz |
| Актау | +77758481014 | inspector14 | inspector.актау@qorgau.kz |
| Темиртау | +77758481015 | inspector15 | inspector.темиртау@qorgau.kz |

## 🏗️ Архитектура проекта

```
fire-safe/
├── qorgau-city/          # Django Backend API
│   ├── src/
│   │   ├── auths/        # Аутентификация и авторизация
│   │   ├── objects/      # Управление объектами
│   │   ├── statements/   # Заявления
│   │   ├── chats/        # Чат система
│   │   └── ...
│   └── Dockerfile
├── qorgau-city-front/    # Vue.js Frontend
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   └── ...
│   └── Dockerfile
└── docker-compose.yml    # Конфигурация Docker
```

## 🔧 Доступные команды Django

### Создание ролей и пользователей
```bash
# Создать все роли, администратора и инспекторов
python manage.py init_project

# Создать только документы
python manage.py create_documents

# Создать ключи документов
python manage.py create_document_keys
```

### Управление пользователями
```bash
# Создать суперпользователя
python manage.py createsuperuser

# Создать тестовых пользователей
python manage.py create_users
```

## 🌐 Доступ к сервисам

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin
- **API Documentation:** http://localhost:8000/swagger/
- **MinIO (S3):** http://localhost:9000

## 📱 Роли в системе

1. **ADMIN** - Администратор системы
2. **INSPECTOR** - Инспектор пожарной безопасности
3. **OBJECT_OWNER** - Собственник объекта
4. **PROVIDER** - Поставщик услуг
5. **CITIZEN** - Гражданин
6. **OPERATOR** - Оператор
7. **FIRE_DEPARTMENT** - Пожарная часть

## 🔐 Безопасность

- Все пароли должны быть изменены в продакшене
- Используйте переменные окружения для чувствительных данных
- Настройте SSL/TLS для HTTPS

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи контейнеров: `docker-compose logs`
2. Убедитесь, что все сервисы запущены: `docker-compose ps`
3. Выполните команду инициализации: `python manage.py init_project`

## 🛠️ Разработка

### Локальная разработка
```bash
# Backend
cd qorgau-city
pip install -r requirements.txt
python manage.py runserver

# Frontend
cd qorgau-city-front
npm install
npm run dev
```

### Тестирование
```bash
# Запуск тестов Django
python manage.py test

# Запуск тестов Vue.js
npm run test
```

## 🔍 Проверка работоспособности

После запуска проверьте:

1. **Логи контейнеров:**
```bash
docker-compose logs -f
```

2. **Статус сервисов:**
```bash
docker-compose ps
```

3. **API Health Check:**
```bash
curl http://localhost:3000/api/health/
```

## 🛠️ Разработка

### Остановка проекта
```bash
docker-compose down
```

### Перезапуск с пересборкой
```bash
docker-compose down
docker-compose up --build -d
```

### Просмотр логов
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f app_backend
docker-compose logs -f frontend
```

### Выполнение команд Django
```bash
# Миграции
docker-compose exec app_backend python manage.py migrate

# Создание суперпользователя
docker-compose exec app_backend python manage.py createsuperuser

# Сбор статики
docker-compose exec app_backend python manage.py collectstatic
```

## 📊 Функциональность

- ✅ **Аутентификация**: JWT токены, SMS подтверждение
- ✅ **Пользователи**: Граждане, инспекторы, поставщики, администраторы
- ✅ **Объекты**: Здания с паспортами безопасности
- ✅ **Документооборот**: Автоматическое создание 14 глав документов
- ✅ **Чат**: Реальное время через WebSocket
- ✅ **Заявления**: Система подачи и обработки заявлений
- ✅ **Файлы**: Загрузка через MinIO S3
- ✅ **API**: Полная документация Swagger

## 🐛 Устранение неполадок

### Проблемы с базой данных
```bash
# Пересоздать базу данных
docker-compose down -v
docker-compose up --build -d
```

### Проблемы с MinIO
```bash
# Проверить создание бакетов
docker-compose exec minio mc ls local/
```

### Проблемы с WebSocket
- Убедитесь, что порт 3001 свободен
- Проверьте подключение: `telnet localhost 3001`

## 📞 Поддержка

При возникновении проблем создайте issue в GitHub репозитории с подробным описанием ошибки и логами.

---

**Версия**: 1.0.0  
**Лицензия**: MIT  
**Автор**: Fire Safe Team 