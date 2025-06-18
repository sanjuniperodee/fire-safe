# 🚀 Инструкции по развертыванию Fire Safety System

## 📋 Предварительные требования

### На сервере должны быть установлены:
- **Docker** (версия 20.10+)
- **Docker Compose** (версия 2.0+)
- **Git**

### Установка Docker на Ubuntu/Debian:
```bash
# Обновление пакетов
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезапуск сессии
newgrp docker
```

## 🔧 Развертывание проекта

### 1. Клонирование и запуск
```bash
git clone https://github.com/sanjuniperodee/fire-safe.git
cd fire-safe
docker-compose up -d
```

### 2. Инициализация системы (ОБЯЗАТЕЛЬНО!)
```bash
# Войти в контейнер Django
docker-compose exec web bash

# Выполнить миграции
python manage.py migrate

# Создать все роли, администратора и инспекторов
python manage.py init_project
```

## 📋 Что создается автоматически

### Роли пользователей:
- ADMIN - Администратор системы
- INSPECTOR - Инспектор пожарной безопасности  
- OBJECT_OWNER - Собственник объекта
- PROVIDER - Поставщик услуг
- CITIZEN - Гражданин
- OPERATOR - Оператор
- FIRE_DEPARTMENT - Пожарная часть

### Администратор:
- Телефон: +77758489538
- Пароль: u4DwQw04
- Email: admin@qorgau.kz

### 15 Инспекторов для городов:
- Алматы: +77758481001 / inspector01
- Нур-Султан: +77758481002 / inspector02
- Шымкент: +77758481003 / inspector03
- Актобе: +77758481004 / inspector04
- Тараз: +77758481005 / inspector05
- Павлодар: +77758481006 / inspector06
- Усть-Каменогорск: +77758481007 / inspector07
- Семей: +77758481008 / inspector08
- Атырау: +77758481009 / inspector09
- Костанай: +77758481010 / inspector10
- Кызылорда: +77758481011 / inspector11
- Уральск: +77758481012 / inspector12
- Петропавловск: +77758481013 / inspector13
- Актау: +77758481014 / inspector14
- Темиртау: +77758481015 / inspector15

### Документы и ключи документов:
- Все необходимые типы документов
- Ключи для генерации документов

## 🌐 Доступ к системе

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- API Docs: http://localhost:8000/swagger/
- MinIO: http://localhost:9000

## 🔧 Полезные команды

### Проверка статуса
```bash
docker-compose ps
docker-compose logs
```

### Остановка и перезапуск
```bash
docker-compose down
docker-compose up -d
```

### Очистка и пересборка
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Вход в контейнеры
```bash
# Django backend
docker-compose exec web bash

# Vue.js frontend  
docker-compose exec frontend sh

# PostgreSQL
docker-compose exec db psql -U postgres -d qorgau_city
```

## 🛠️ Дополнительные команды Django

```bash
# Создать суперпользователя
python manage.py createsuperuser

# Сбросить пароль пользователя
python manage.py changepassword +77758489538

# Собрать статические файлы
python manage.py collectstatic

# Проверить миграции
python manage.py showmigrations

# Создать миграции
python manage.py makemigrations
```

## 🔐 Безопасность для продакшена

1. Измените все пароли по умолчанию
2. Настройте переменные окружения
3. Используйте HTTPS
4. Настройте файрвол
5. Регулярно обновляйте зависимости

## 📞 Диагностика проблем

### Если контейнеры не запускаются:
```bash
docker-compose logs web
docker-compose logs db
```

### Если нет доступа к API:
```bash
# Проверить что Django запущен
docker-compose exec web python manage.py check

# Проверить миграции
docker-compose exec web python manage.py showmigrations
```

### Если фронтенд не работает:
```bash
docker-compose logs frontend
```

## ✅ Проверка успешного развертывания

1. Откройте http://localhost:3000 - должен загрузиться фронтенд
2. Откройте http://localhost:8000/admin - должна открыться админка Django
3. Войдите с учетными данными администратора
4. Проверьте что в админке есть пользователи и роли
5. Попробуйте войти как инспектор через фронтенд

## 🔍 Проверка работоспособности

### Проверка статуса контейнеров:
```bash
docker-compose ps
```

### Проверка логов:
```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f app_backend
docker-compose logs -f frontend
docker-compose logs -f websocket_server
```

### Проверка API:
```bash
curl http://localhost:3000/api/v1/auth/health/
```

### Проверка WebSocket:
```bash
# Установка wscat (если нужно)
npm install -g wscat

# Тест WebSocket соединения
wscat -c ws://localhost:3001/ws/test/
```

## 🛠️ Управление проектом

### Остановка всех сервисов:
```bash
docker-compose down
```

### Перезапуск с пересборкой:
```bash
docker-compose down
docker-compose up --build -d
```

### Просмотр использования ресурсов:
```bash
docker stats
```

### Очистка неиспользуемых Docker данных:
```bash
docker system prune -a
```

## 🗄️ Управление базой данных

### Создание резервной копии:
```bash
docker-compose exec db pg_dump -U qorgau_user qorgau_city > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Восстановление из резервной копии:
```bash
docker-compose exec -T db psql -U qorgau_user qorgau_city < backup_file.sql
```

### Выполнение Django команд:
```bash
# Миграции
docker-compose exec app_backend python manage.py migrate

# Создание суперпользователя
docker-compose exec app_backend python manage.py createsuperuser

# Сбор статических файлов
docker-compose exec app_backend python manage.py collectstatic

# Django shell
docker-compose exec app_backend python manage.py shell
```

## 📊 Мониторинг

### Просмотр логов в реальном времени:
```bash
# Все сервисы
docker-compose logs -f --tail=100

# Только ошибки
docker-compose logs -f | grep -i error
```

### Мониторинг ресурсов:
```bash
# Использование CPU и памяти
docker stats --no-stream

# Размер дисков
df -h
docker system df
```

## 🐛 Устранение неполадок

### Проблема: Контейнер не запускается
```bash
# Проверить логи
docker-compose logs service_name

# Перезапустить конкретный сервис
docker-compose restart service_name
```

### Проблема: База данных недоступна
```bash
# Проверить подключение к БД
docker-compose exec app_backend python manage.py check --database default

# Пересоздать БД (ОСТОРОЖНО - удалит все данные!)
docker-compose down -v
docker-compose up --build -d
```

### Проблема: Порты заняты
```bash
# Найти процесс, использующий порт
sudo netstat -tulpn | grep :8080

# Остановить процесс
sudo kill -9 PID
```

### Проблема: Недостаточно места на диске
```bash
# Очистка Docker
docker system prune -a --volumes

# Очистка логов
sudo truncate -s 0 /var/lib/docker/containers/*/*-json.log
```

## 📞 Поддержка

При возникновении проблем:

1. **Соберите информацию**:
```bash
# Версии
docker --version
docker-compose --version

# Статус сервисов
docker-compose ps

# Логи с ошибками
docker-compose logs | grep -i error > error_logs.txt
```

2. **Создайте issue** в GitHub репозитории с:
   - Описанием проблемы
   - Шагами для воспроизведения
   - Логами ошибок
   - Информацией о системе

---

**🎯 Успешного развертывания!** 