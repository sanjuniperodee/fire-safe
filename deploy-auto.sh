#!/bin/bash

# 🚀 Fire Safety System - Автоматическое развертывание (Smart Version)

echo "🔥 Fire Safety Management System - Smart Deployment Script"
echo "========================================================"

# Проверка что мы в правильной директории
if [ ! -f "docker-compose.yml" ] || [ ! -d "qorgau-city" ] || [ ! -d "qorgau-city-front" ]; then
    echo "❌ Ошибка: Скрипт должен запускаться из корневой директории проекта fire-safe"
    echo "💡 Убедитесь что вы находитесь в директории с файлами docker-compose.yml, qorgau-city/ и qorgau-city-front/"
    echo "🔍 Текущая директория: $(pwd)"
    echo "📁 Содержимое текущей директории:"
    ls -la
    exit 1
fi

# Проверка существования Dockerfile'ов
if [ ! -f "qorgau-city/docker/Dockerfile" ]; then
    echo "❌ Не найден Dockerfile для backend: qorgau-city/docker/Dockerfile"
    exit 1
fi

if [ ! -f "qorgau-city-front/Dockerfile" ]; then
    echo "❌ Не найден Dockerfile для frontend: qorgau-city-front/Dockerfile"
    exit 1
fi

echo "✅ Проверка структуры проекта пройдена"

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

# Проверка Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose."
    exit 1
fi

echo "✅ Docker и Docker Compose найдены"

# Проверка версии Docker Compose и выбор файла
COMPOSE_VERSION=$(docker-compose --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
echo "ℹ️ Docker Compose версия: $COMPOSE_VERSION"

# Определяем какой файл использовать
COMPOSE_FILE="docker-compose.yml"
echo "🔍 Проверяем совместимость docker-compose.yml..."
if ! docker-compose -f docker-compose.yml config &> /dev/null; then
    echo "⚠️ Основной docker-compose.yml не поддерживается, используем legacy версию..."
    COMPOSE_FILE="docker-compose-legacy.yml"
    
    if ! docker-compose -f docker-compose-legacy.yml config &> /dev/null; then
        echo "❌ Ни один из docker-compose файлов не работает. Проверьте версию Docker Compose."
        echo "💡 Попробуйте обновить Docker Compose до версии 1.27+ или 2.0+"
        echo "🔍 Вывод ошибки конфигурации:"
        docker-compose -f docker-compose.yml config
        exit 1
    fi
fi

echo "✅ Используем файл: $COMPOSE_FILE"

# Остановка существующих контейнеров ТОЛЬКО этого проекта
echo "🔄 Остановка существующих контейнеров проекта..."
docker-compose -f $COMPOSE_FILE down

# Безопасная очистка - только неиспользуемые ресурсы
echo "🧹 Очистка неиспользуемых ресурсов..."
docker system prune -f --filter "label!=keep"

# Сборка и запуск контейнеров
echo "🏗️ Сборка и запуск контейнеров..."
echo "📋 Используемый файл: $COMPOSE_FILE"
echo "📁 Рабочая директория: $(pwd)"

if ! docker-compose -f $COMPOSE_FILE up -d --build; then
    echo "❌ Ошибка при запуске контейнеров. Проверьте логи:"
    docker-compose -f $COMPOSE_FILE logs
    echo ""
    echo "🔍 Дополнительная диагностика:"
    echo "- Проверьте что Docker запущен: docker ps"
    echo "- Проверьте доступное место на диске: df -h"
    echo "- Проверьте права доступа к файлам: ls -la qorgau-city/docker/"
    exit 1
fi

# Ожидание запуска всех сервисов
echo "⏳ Ожидание запуска всех сервисов..."
sleep 45

# Проверка статуса контейнеров
echo "🔍 Проверка статуса контейнеров..."
docker-compose -f $COMPOSE_FILE ps

# Проверка, что основные сервисы запущены
if ! docker-compose -f $COMPOSE_FILE ps | grep -q "web.*Up"; then
    echo "❌ Веб-сервер не запущен. Проверяем логи..."
    docker-compose -f $COMPOSE_FILE logs web
    exit 1
fi

if ! docker-compose -f $COMPOSE_FILE ps | grep -q "db.*Up"; then
    echo "❌ База данных не запущена. Проверяем логи..."
    docker-compose -f $COMPOSE_FILE logs db
    exit 1
fi

# Выполнение миграций
echo "📋 Выполнение миграций..."
if ! docker-compose -f $COMPOSE_FILE exec -T web python manage.py migrate; then
    echo "❌ Ошибка при выполнении миграций. Попробуем еще раз через 10 секунд..."
    sleep 10
    if ! docker-compose -f $COMPOSE_FILE exec -T web python manage.py migrate; then
        echo "❌ Миграции не удались. Проверьте логи:"
        docker-compose -f $COMPOSE_FILE logs web
        exit 1
    fi
fi

# Инициализация проекта
echo "🎯 Инициализация проекта (создание ролей, админа, инспекторов)..."
if ! docker-compose -f $COMPOSE_FILE exec -T web python manage.py init_project; then
    echo "❌ Ошибка при инициализации проекта. Проверьте логи:"
    docker-compose -f $COMPOSE_FILE logs web
    exit 1
fi

# Финальная проверка статуса
echo "🔍 Финальная проверка статуса контейнеров..."
docker-compose -f $COMPOSE_FILE ps

echo ""
echo "✅ Развертывание завершено!"
echo ""
echo "🌐 Доступ к системе:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   Admin:    http://localhost:8000/admin"
echo "   API Docs: http://localhost:8000/swagger/"
echo "   MinIO:    http://localhost:9001"
echo ""
echo "🔑 Учетные данные:"
echo "   Админ: +77758489538 / u4DwQw04"
echo "   Инспекторы: +77758481001-015 / inspector01-15"
echo ""
echo "📚 Подробная документация в README.md"
echo ""
echo "🔧 Полезные команды:"
echo "   Логи всех сервисов: docker-compose -f $COMPOSE_FILE logs"
echo "   Логи конкретного сервиса: docker-compose -f $COMPOSE_FILE logs web"
echo "   Перезапуск: docker-compose -f $COMPOSE_FILE restart"
echo "   Остановка: docker-compose -f $COMPOSE_FILE down" 