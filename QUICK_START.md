# 🚀 Быстрый запуск Fire Safety System

## Одной командой:
```bash
git clone https://github.com/sanjuniperodee/fire-safe.git && cd fire-safe && docker-compose up -d
```

## Инициализация (ОБЯЗАТЕЛЬНО!):
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py init_project
```

## 🔑 Учетные данные:

**Админ:** +77758489538 / u4DwQw04

**Инспекторы:**
- Алматы: +77758481001 / inspector01
- Нур-Султан: +77758481002 / inspector02
- Шымкент: +77758481003 / inspector03
- И т.д. (всего 15 городов)

## 🌐 Доступ:
- Frontend: http://localhost:3000
- Admin: http://localhost:8000/admin
- API: http://localhost:8000/swagger/

## ✅ Готово!
Система создаст автоматически:
- 7 ролей пользователей
- 1 администратора
- 15 инспекторов по городам
- Все необходимые документы 