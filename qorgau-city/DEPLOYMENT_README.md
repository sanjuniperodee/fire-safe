# 🚀 Qorgau City - Руководство по развертыванию

## Быстрый старт

Этот проект настроен для полностью автоматического развертывания. Все необходимые данные создаются автоматически.

### 1. Клонирование проекта
```bash
git clone <repository-url>
cd qorgau-city
```

### 2. Настройка окружения
```bash
# Копируем пример конфигурации
cp docker/example.env docker/.env

# При необходимости отредактируйте docker/.env
```

### 3. Запуск проекта
```bash
# Запускаем все сервисы
docker-compose up -d

# Следим за логами инициализации
docker-compose logs -f app_backend
```

### 4. Проверка работы
- **Backend API**: http://localhost:3000
- **WebSocket**: ws://localhost:3001
- **MinIO Console**: http://localhost:9001
- **Admin Panel**: http://localhost:3000/admin/

## 🔑 Учетные данные по умолчанию

### 👤 Администратор системы
- **Телефон**: `+77758489538`
- **Пароль**: `u4DwQw04`
- **Email**: `admin@qorgau.kz`
- **Роли**: Администратор, Суперпользователь

### 👨‍💼 Инспекторы по городам

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

## 🏗️ Архитектура системы

### Сервисы
- **app_backend** (порт 3000) - Django REST API
- **websocket_server** (порт 3001) - WebSocket сервер для чатов
- **database_backend** (порт 5432) - PostgreSQL база данных
- **redis_backend** (порт 6380) - Redis для кеширования и Celery
- **minio** (порты 9000/9001) - MinIO для хранения файлов
- **celery_worker** - Фоновые задачи
- **celery_beat** - Планировщик задач

### Автоматическая инициализация
При первом запуске автоматически создаются:
- ✅ 4 роли пользователей (Админ, Инспектор, Поставщик, Пользователь)
- ✅ 15 городов Казахстана
- ✅ Администратор системы
- ✅ 15 инспекторов (по одному на каждый город)
- ✅ 26 типов документов для паспортов зданий
- ✅ 225+ ключей документов
- ✅ Корзины MinIO (isec, public, static)

## 🔧 Настройка для продакшена

### 1. Переменные окружения
Отредактируйте `docker/.env`:
```env
# Безопасность
DEBUG=0
SECRET_KEY=your-super-secret-key-here

# База данных
POSTGRES_DB=qorgau_city_prod
POSTGRES_USER=qorgau_user
POSTGRES_PASSWORD=super-secure-password

# MinIO
MINIO_ACCESS_KEY=your-minio-access-key
MINIO_SECRET_KEY=your-minio-secret-key

# Домен
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 2. Nginx конфигурация
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # API
    location /api/ {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket
    location /ws/ {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # Статические файлы
    location /static/ {
        alias /path/to/qorgau-city/staticfiles/;
    }

    # Frontend
    location / {
        root /path/to/qorgau-city-front/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

### 3. SSL сертификат
```bash
# Certbot для Let's Encrypt
sudo certbot --nginx -d yourdomain.com
```

## 🐛 Решение проблем

### Проблемы с базой данных
```bash
# Пересоздать базу данных
docker-compose down -v
docker-compose up -d database_backend
docker-compose up app_backend
```

### Проблемы с MinIO
```bash
# Пересоздать корзины
docker-compose up createbuckets
```

### Проблемы с миграциями
```bash
# Выполнить миграции вручную
docker-compose exec app_backend python manage.py migrate
```

### Проблемы с инициализацией
```bash
# Повторная инициализация данных
docker-compose exec app_backend python manage.py init_project
```

### Проблемы с WebSocket
```bash
# Проверить WebSocket сервер
docker-compose logs websocket_server
```

## 📊 Мониторинг

### Проверка статуса сервисов
```bash
docker-compose ps
```

### Просмотр логов
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f app_backend
docker-compose logs -f websocket_server
```

### Проверка базы данных
```bash
docker-compose exec database_backend psql -U postgres -d qorgau_city -c "
SELECT 
    (SELECT COUNT(*) FROM auths_userrole) as roles,
    (SELECT COUNT(*) FROM auths_city) as cities,
    (SELECT COUNT(*) FROM auths_customuser) as users,
    (SELECT COUNT(*) FROM objects_document) as documents,
    (SELECT COUNT(*) FROM objects_documentkey) as document_keys,
    (SELECT COUNT(*) FROM chats_chatroom) as chat_rooms,
    (SELECT COUNT(*) FROM chats_message) as messages;
"
```

## 🔄 Обновление проекта

### 1. Обновление кода
```bash
git pull origin main
docker-compose build
docker-compose up -d
```

### 2. Применение новых миграций
```bash
docker-compose exec app_backend python manage.py migrate
```

### 3. Обновление статических файлов
```bash
docker-compose exec app_backend python manage.py collectstatic --noinput
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи сервисов
2. Убедитесь, что все порты свободны
3. Проверьте конфигурацию в `docker/.env`
4. Пересоздайте контейнеры при необходимости

---

**Система готова к работе после выполнения команды `docker-compose up -d`!** 🎉 