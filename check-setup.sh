#!/bin/bash

# 🔍 Fire Safety System - Проверка готовности к развертыванию

echo "🔍 Fire Safety System - Setup Check"
echo "==================================="

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Проверка структуры проекта...${NC}"

# Проверка основных файлов и директорий
checks=(
    "docker-compose.yml:Основной файл Docker Compose"
    "docker-compose-legacy.yml:Legacy файл Docker Compose"
    "qorgau-city/:Директория Django backend"
    "qorgau-city-front/:Директория Vue.js frontend"
    "qorgau-city/docker/Dockerfile:Dockerfile для backend"
    "qorgau-city-front/Dockerfile:Dockerfile для frontend"
    "deploy.sh:Скрипт развертывания для Linux/macOS"
    "deploy-auto.sh:Умный скрипт развертывания"
    "deploy.ps1:Скрипт развертывания для Windows"
)

for check in "${checks[@]}"; do
    file=$(echo $check | cut -d: -f1)
    desc=$(echo $check | cut -d: -f2)
    
    if [ -e "$file" ]; then
        echo -e "  ✅ ${GREEN}$desc${NC} - найден"
    else
        echo -e "  ❌ ${RED}$desc${NC} - НЕ НАЙДЕН: $file"
    fi
done

echo ""
echo -e "${BLUE}2. Проверка Docker...${NC}"

# Проверка Docker
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo -e "  ✅ ${GREEN}Docker установлен:${NC} $DOCKER_VERSION"
    
    # Проверка что Docker запущен
    if docker ps &> /dev/null; then
        echo -e "  ✅ ${GREEN}Docker сервис запущен${NC}"
    else
        echo -e "  ❌ ${RED}Docker сервис не запущен${NC}"
        echo -e "     💡 Запустите Docker Desktop или systemctl start docker"
    fi
else
    echo -e "  ❌ ${RED}Docker не установлен${NC}"
    echo -e "     💡 Установите Docker: https://docs.docker.com/get-docker/"
fi

# Проверка Docker Compose
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    echo -e "  ✅ ${GREEN}Docker Compose установлен:${NC} $COMPOSE_VERSION"
    
    # Проверка версии
    VERSION_NUM=$(docker-compose --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
    if [ -n "$VERSION_NUM" ]; then
        echo -e "  ℹ️  ${BLUE}Версия Docker Compose:${NC} $VERSION_NUM"
    fi
else
    echo -e "  ❌ ${RED}Docker Compose не установлен${NC}"
    echo -e "     💡 Установите Docker Compose: https://docs.docker.com/compose/install/"
fi

echo ""
echo -e "${BLUE}3. Проверка конфигурации Docker Compose...${NC}"

# Проверка основного файла
if docker-compose -f docker-compose.yml config &> /dev/null; then
    echo -e "  ✅ ${GREEN}docker-compose.yml - валидный${NC}"
else
    echo -e "  ⚠️  ${YELLOW}docker-compose.yml - проблемы с совместимостью${NC}"
fi

# Проверка legacy файла
if [ -f "docker-compose-legacy.yml" ]; then
    if docker-compose -f docker-compose-legacy.yml config &> /dev/null; then
        echo -e "  ✅ ${GREEN}docker-compose-legacy.yml - валидный${NC}"
    else
        echo -e "  ❌ ${RED}docker-compose-legacy.yml - ошибки конфигурации${NC}"
    fi
fi

echo ""
echo -e "${BLUE}4. Проверка ресурсов системы...${NC}"

# Проверка места на диске
DISK_USAGE=$(df -h . | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 90 ]; then
    echo -e "  ✅ ${GREEN}Свободное место на диске: достаточно${NC} (использовано ${DISK_USAGE}%)"
else
    echo -e "  ⚠️  ${YELLOW}Мало места на диске${NC} (использовано ${DISK_USAGE}%)"
    echo -e "     💡 Освободите место на диске"
fi

# Проверка портов
PORTS=(3000 8000 8001 5432 6380 9000 9001)
echo -e "  🔍 ${BLUE}Проверка портов...${NC}"

for port in "${PORTS[@]}"; do
    if command -v netstat &> /dev/null; then
        if netstat -tuln | grep -q ":$port "; then
            echo -e "    ⚠️  ${YELLOW}Порт $port занят${NC}"
        else
            echo -e "    ✅ ${GREEN}Порт $port свободен${NC}"
        fi
    elif command -v ss &> /dev/null; then
        if ss -tuln | grep -q ":$port "; then
            echo -e "    ⚠️  ${YELLOW}Порт $port занят${NC}"
        else
            echo -e "    ✅ ${GREEN}Порт $port свободен${NC}"
        fi
    else
        echo -e "    ℹ️  ${BLUE}Не удается проверить порт $port (netstat/ss не найден)${NC}"
    fi
done

echo ""
echo -e "${BLUE}5. Рекомендации по запуску...${NC}"

if [ -f "docker-compose.yml" ] && [ -d "qorgau-city" ] && [ -d "qorgau-city-front" ]; then
    if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
        echo -e "  🚀 ${GREEN}Система готова к развертыванию!${NC}"
        echo ""
        echo -e "  📋 ${BLUE}Рекомендуемые команды для запуска:${NC}"
        echo -e "     chmod +x deploy-auto.sh && ./deploy-auto.sh"
        echo -e "     ${YELLOW}или${NC}"
        echo -e "     chmod +x deploy.sh && ./deploy.sh"
        echo -e "     ${YELLOW}или${NC}"
        echo -e "     docker-compose up -d --build"
    else
        echo -e "  ❌ ${RED}Установите Docker и Docker Compose перед запуском${NC}"
    fi
else
    echo -e "  ❌ ${RED}Запустите скрипт из корневой директории проекта fire-safe${NC}"
fi

echo ""
echo -e "${BLUE}📚 Дополнительная помощь:${NC}"
echo -e "   - README.md - полная документация"
echo -e "   - TROUBLESHOOTING.md - решение проблем"
echo -e "   - QUICK_START.md - быстрый старт" 