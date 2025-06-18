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

# Остановка существующих контейнеров
echo "🔄 Остановка существующих контейнеров..."
docker-compose down

# Сборка и запуск контейнеров
echo "🏗️ Сборка и запуск контейнеров..."
docker-compose up -d --build

# Ожидание запуска базы данных
echo "⏳ Ожидание запуска базы данных..."
sleep 30

# Выполнение миграций
echo "📋 Выполнение миграций..."
docker-compose exec -T web python manage.py migrate

# Инициализация проекта
echo "🎯 Инициализация проекта (создание ролей, админа, инспекторов)..."
docker-compose exec -T web python manage.py init_project

# Проверка статуса
echo "🔍 Проверка статуса контейнеров..."
docker-compose ps

echo ""
echo "✅ Развертывание завершено!"
echo ""
echo "🌐 Доступ к системе:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   Admin:    http://localhost:8000/admin"
echo "   API Docs: http://localhost:8000/swagger/"
echo ""
echo "🔑 Учетные данные:"
echo "   Админ: +77758489538 / u4DwQw04"
echo "   Инспекторы: +77758481001-015 / inspector01-15"
echo ""
echo "📚 Подробная документация в README.md" 