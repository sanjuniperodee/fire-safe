# 🔧 Устранение неполадок Fire Safety System

## 🚨 Частые проблемы и решения

### 0. Папка qorgau-city пустая или не найдена

#### Проблема: При запуске появляется ошибка о том, что папка `qorgau-city` пустая или не найдена

**Причины:**
- Скрипт запущен не из корневой директории проекта
- Неполное клонирование репозитория
- Проблемы с Git LFS (если используется)

**Решение:**
```bash
# 1. Убедитесь что вы в правильной директории
pwd
ls -la

# Должны видеть: docker-compose.yml, qorgau-city/, qorgau-city-front/

# 2. Если папки нет - проверьте клонирование
git status
git pull

# 3. Проверьте содержимое папок
ls -la qorgau-city/
ls -la qorgau-city-front/

# 4. Запустите диагностику
chmod +x check-setup.sh
./check-setup.sh

# 5. Если папки все еще пустые, переклонируйте репозиторий
cd ..
git clone <ваш-репозиторий> fire-safe-new
cd fire-safe-new
```

### 1. Ошибки Docker Compose

#### Проблема: "Unsupported config option" или "Version is unsupported"
```
ERROR: The Compose file './docker-compose.yml' is invalid because:
Unsupported config option for services: 'celery_beat'
```
или
```
ERROR: Version in "./docker-compose.yml" is unsupported
```

**Решения:**

1. **Используйте умный скрипт развертывания (рекомендуется):**
```bash
./deploy-auto.sh  # Автоматически выберет правильную версию
```

2. **Используйте legacy версию для старых Docker Compose:**
```bash
docker-compose -f docker-compose-legacy.yml up -d
```

3. **Обновите Docker Compose:**
- Проверьте версию: `docker-compose --version`
- Обновите до версии 1.27+ или 2.0+

#### Проблема: Контейнеры не запускаются
```bash
# Проверьте логи всех сервисов
docker-compose logs

# Проверьте логи конкретного сервиса
docker-compose logs web
docker-compose logs db
```

**Общие решения:**
```bash
# Полная очистка и перезапуск
docker-compose down -v
docker system prune -f
docker-compose up -d --build
```

### 2. Проблемы с базой данных

#### Проблема: "Connection refused" или "Database not ready"
```bash
# Проверьте статус базы данных
docker-compose logs db

# Перезапустите только базу данных
docker-compose restart db

# Подождите 30 секунд и попробуйте миграции снова
docker-compose exec web python manage.py migrate
```

#### Проблема: Ошибки миграций
```bash
# Проверьте подключение к БД
docker-compose exec web python manage.py dbshell

# Сбросьте миграции (ОСТОРОЖНО - удалит данные!)
docker-compose exec web python manage.py migrate --fake-initial

# Или пересоздайте базу данных
docker-compose down -v
docker-compose up -d
```

### 3. Проблемы с инициализацией

#### Проблема: "init_project" не работает
```bash
# Убедитесь, что миграции выполнены
docker-compose exec web python manage.py showmigrations

# Проверьте, что база данных доступна
docker-compose exec web python manage.py check --database

# Попробуйте создать роли отдельно
docker-compose exec web python manage.py shell -c "
from auths.models import CustomUserRole
import auths
for role_choice in auths.Role.choices:
    role_name, display_name = role_choice
    role, created = CustomUserRole.objects.get_or_create(role=role_name)
    print(f'Role {display_name}: {\"Created\" if created else \"Exists\"}')
"
```

### 4. Проблемы с портами

#### Проблема: "Port already in use"
```bash
# Найдите процессы, использующие порты
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :5432

# Остановите конфликтующие сервисы
sudo fuser -k 8000/tcp
sudo fuser -k 3000/tcp

# Или измените порты в docker-compose.yml
```

### 5. Проблемы с MinIO

#### Проблема: MinIO не создает бакеты
```bash
# Проверьте логи MinIO
docker-compose logs minio
docker-compose logs minio-init

# Пересоздайте MinIO контейнер
docker-compose stop minio minio-init
docker-compose rm minio minio-init
docker-compose up -d minio minio-init
```

### 6. Проблемы с фронтендом

#### Проблема: Frontend не загружается
```bash
# Проверьте логи фронтенда
docker-compose logs frontend

# Пересоберите фронтенд
docker-compose stop frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

## 🔍 Диагностические команды

### Автоматическая проверка системы (рекомендуется)
```bash
# Запустите скрипт проверки готовности
chmod +x check-setup.sh
./check-setup.sh
```

### Ручная проверка системы
```bash
# Проверка версий
docker --version
docker-compose --version

# Проверка ресурсов
docker system df
docker system info

# Статус всех контейнеров
docker-compose ps

# Логи всех сервисов
docker-compose logs --tail=50
```

### Проверка Django
```bash
# Вход в контейнер Django
docker-compose exec web bash

# Проверка Django
python manage.py check

# Проверка миграций
python manage.py showmigrations

# Проверка подключения к БД
python manage.py dbshell

# Django shell
python manage.py shell
```

### Проверка сети
```bash
# Проверка сетевого подключения между контейнерами
docker-compose exec web ping db
docker-compose exec web ping redis
docker-compose exec web ping minio

# Проверка портов изнутри контейнера
docker-compose exec web netstat -tulpn
```

## 🛠️ Полная переустановка

Если ничего не помогает, выполните полную переустановку:

```bash
# 1. Остановите и удалите все контейнеры
docker-compose down -v

# 2. Удалите все образы проекта
docker images | grep fire-safe | awk '{print $3}' | xargs docker rmi -f

# 3. Очистите систему Docker
docker system prune -a -f

# 4. Удалите volumes (ОСТОРОЖНО - удалит все данные!)
docker volume prune -f

# 5. Пересоберите проект
docker-compose build --no-cache

# 6. Запустите заново
docker-compose up -d
```

## 📞 Получение помощи

### Сбор информации для отчета об ошибке
```bash
# Создайте файл с диагностической информацией
echo "=== SYSTEM INFO ===" > debug_info.txt
docker --version >> debug_info.txt
docker-compose --version >> debug_info.txt
echo "" >> debug_info.txt

echo "=== CONTAINER STATUS ===" >> debug_info.txt
docker-compose ps >> debug_info.txt
echo "" >> debug_info.txt

echo "=== LOGS ===" >> debug_info.txt
docker-compose logs --tail=100 >> debug_info.txt
```

### Контакты
- GitHub Issues: https://github.com/sanjuniperodee/fire-safe/issues
- Email: support@qorgau.kz

## ⚡ Быстрые решения

| Проблема | Быстрое решение |
|----------|----------------|
| Контейнеры не запускаются | `docker-compose down -v && docker-compose up -d --build` |
| БД недоступна | `docker-compose restart db && sleep 30` |
| Порт занят | `sudo fuser -k 8000/tcp && docker-compose restart web` |
| Миграции не работают | `docker-compose exec web python manage.py migrate --fake-initial` |
| Frontend не загружается | `docker-compose restart frontend` |
| MinIO не работает | `docker-compose restart minio minio-init` | 