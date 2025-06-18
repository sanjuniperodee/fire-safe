#!/bin/bash

# 🚀 Fire Safety System - Автоматическое развертывание

echo "🔥 Fire Safety Management System - Deployment Script"
echo "=================================================="

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

# Проверка версии Docker Compose
COMPOSE_VERSION=$(docker-compose --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
echo "ℹ️ Docker Compose версия: $COMPOSE_VERSION"

# Остановка существующих контейнеров
echo "🔄 Остановка существующих контейнеров..."
docker-compose down -v

# Очистка старых образов (опционально)
echo "🧹 Очистка старых образов..."
docker system prune -f

# Сборка и запуск контейнеров
echo "🏗️ Сборка и запуск контейнеров..."
if ! docker-compose up -d --build; then
    echo "❌ Ошибка при запуске контейнеров. Проверьте логи:"
    docker-compose logs
    exit 1
fi

# Ожидание запуска всех сервисов
echo "⏳ Ожидание запуска всех сервисов..."
sleep 45

# Проверка статуса контейнеров
echo "🔍 Проверка статуса контейнеров..."
docker-compose ps

# Проверка, что основные сервисы запущены
if ! docker-compose ps | grep -q "web.*Up"; then
    echo "❌ Веб-сервер не запущен. Проверяем логи..."
    docker-compose logs web
    exit 1
fi

if ! docker-compose ps | grep -q "db.*Up"; then
    echo "❌ База данных не запущена. Проверяем логи..."
    docker-compose logs db
    exit 1
fi

# Выполнение миграций
echo "📋 Выполнение миграций..."
if ! docker-compose exec -T web python manage.py migrate; then
    echo "❌ Ошибка при выполнении миграций. Попробуем еще раз через 10 секунд..."
    sleep 10
    if ! docker-compose exec -T web python manage.py migrate; then
        echo "❌ Миграции не удались. Проверьте логи:"
        docker-compose logs web
        exit 1
    fi
fi

# Инициализация проекта
echo "🎯 Инициализация проекта (создание ролей, админа, инспекторов)..."
if ! docker-compose exec -T web python manage.py init_project; then
    echo "❌ Ошибка при инициализации проекта. Проверьте логи:"
    docker-compose logs web
    exit 1
fi

# Финальная проверка статуса
echo "🔍 Финальная проверка статуса контейнеров..."
docker-compose ps

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
echo "   Логи всех сервисов: docker-compose logs"
echo "   Логи конкретного сервиса: docker-compose logs web"
echo "   Перезапуск: docker-compose restart"
echo "   Остановка: docker-compose down" 