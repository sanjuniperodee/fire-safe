# 🚀 Fire Safety System - Автоматическое развертывание (Windows)

Write-Host "🔥 Fire Safety Management System - Deployment Script" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Проверка Docker
try {
    docker --version | Out-Null
    Write-Host "✅ Docker найден" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker не установлен. Пожалуйста, установите Docker Desktop." -ForegroundColor Red
    exit 1
}

# Проверка Docker Compose
try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose найден" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose не найден. Пожалуйста, установите Docker Compose." -ForegroundColor Red
    exit 1
}

# Остановка существующих контейнеров
Write-Host "🔄 Остановка существующих контейнеров..." -ForegroundColor Yellow
docker-compose down

# Сборка и запуск контейнеров
Write-Host "🏗️ Сборка и запуск контейнеров..." -ForegroundColor Yellow
docker-compose up -d --build

# Ожидание запуска базы данных
Write-Host "⏳ Ожидание запуска базы данных..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Выполнение миграций
Write-Host "📋 Выполнение миграций..." -ForegroundColor Yellow
docker-compose exec -T web python manage.py migrate

# Инициализация проекта
Write-Host "🎯 Инициализация проекта (создание ролей, админа, инспекторов)..." -ForegroundColor Yellow
docker-compose exec -T web python manage.py init_project

# Проверка статуса
Write-Host "🔍 Проверка статуса контейнеров..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "✅ Развертывание завершено!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Доступ к системе:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   Admin:    http://localhost:8000/admin" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/swagger/" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Учетные данные:" -ForegroundColor Cyan
Write-Host "   Админ: +77758489538 / u4DwQw04" -ForegroundColor White
Write-Host "   Инспекторы: +77758481001-015 / inspector01-15" -ForegroundColor White
Write-Host ""
Write-Host "📚 Подробная документация в README.md" -ForegroundColor Cyan

# Открыть браузер
$openBrowser = Read-Host "Открыть браузер? (y/n)"
if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
    Start-Process "http://localhost:3000"
    Start-Process "http://localhost:8000/admin"
} 