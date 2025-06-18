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

# Проверка версии Docker Compose
$composeVersion = docker-compose --version
Write-Host "ℹ️ $composeVersion" -ForegroundColor Blue

# Остановка существующих контейнеров
Write-Host "🔄 Остановка существующих контейнеров..." -ForegroundColor Yellow
docker-compose down -v

# Очистка старых образов
Write-Host "🧹 Очистка старых образов..." -ForegroundColor Yellow
docker system prune -f

# Сборка и запуск контейнеров
Write-Host "🏗️ Сборка и запуск контейнеров..." -ForegroundColor Yellow
$buildResult = docker-compose up -d --build
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Ошибка при запуске контейнеров. Проверьте логи:" -ForegroundColor Red
    docker-compose logs
    exit 1
}

# Ожидание запуска всех сервисов
Write-Host "⏳ Ожидание запуска всех сервисов..." -ForegroundColor Yellow
Start-Sleep -Seconds 45

# Проверка статуса контейнеров
Write-Host "🔍 Проверка статуса контейнеров..." -ForegroundColor Yellow
docker-compose ps

# Проверка, что основные сервисы запущены
$webStatus = docker-compose ps | Select-String "web.*Up"
if (-not $webStatus) {
    Write-Host "❌ Веб-сервер не запущен. Проверяем логи..." -ForegroundColor Red
    docker-compose logs web
    exit 1
}

$dbStatus = docker-compose ps | Select-String "db.*Up"
if (-not $dbStatus) {
    Write-Host "❌ База данных не запущена. Проверяем логи..." -ForegroundColor Red
    docker-compose logs db
    exit 1
}

# Выполнение миграций
Write-Host "📋 Выполнение миграций..." -ForegroundColor Yellow
$migrateResult = docker-compose exec -T web python manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Ошибка при выполнении миграций. Попробуем еще раз через 10 секунд..." -ForegroundColor Red
    Start-Sleep -Seconds 10
    $migrateResult = docker-compose exec -T web python manage.py migrate
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Миграции не удались. Проверьте логи:" -ForegroundColor Red
        docker-compose logs web
        exit 1
    }
}

# Инициализация проекта
Write-Host "🎯 Инициализация проекта (создание ролей, админа, инспекторов)..." -ForegroundColor Yellow
$initResult = docker-compose exec -T web python manage.py init_project
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Ошибка при инициализации проекта. Проверьте логи:" -ForegroundColor Red
    docker-compose logs web
    exit 1
}

# Финальная проверка статуса
Write-Host "🔍 Финальная проверка статуса контейнеров..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "✅ Развертывание завершено!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Доступ к системе:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   Admin:    http://localhost:8000/admin" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/swagger/" -ForegroundColor White
Write-Host "   MinIO:    http://localhost:9001" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Учетные данные:" -ForegroundColor Cyan
Write-Host "   Админ: +77758489538 / u4DwQw04" -ForegroundColor White
Write-Host "   Инспекторы: +77758481001-015 / inspector01-15" -ForegroundColor White
Write-Host ""
Write-Host "📚 Подробная документация в README.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔧 Полезные команды:" -ForegroundColor Cyan
Write-Host "   Логи всех сервисов: docker-compose logs" -ForegroundColor White
Write-Host "   Логи конкретного сервиса: docker-compose logs web" -ForegroundColor White
Write-Host "   Перезапуск: docker-compose restart" -ForegroundColor White
Write-Host "   Остановка: docker-compose down" -ForegroundColor White

# Открыть браузер
Write-Host ""
$openBrowser = Read-Host "Открыть браузер? (y/n)"
if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
    Start-Process "http://localhost:3000"
    Start-Process "http://localhost:8000/admin"
} 