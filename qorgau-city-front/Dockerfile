# Базовый образ Node.js
FROM node:18-alpine

# Установим рабочую директорию
WORKDIR /app

# Копируем package.json и yarn.lock
COPY package.json yarn.lock ./

# Устанавливаем зависимости
RUN yarn install

# Копируем остальной код
COPY . .

# Открываем порт Vite (по умолчанию 5173)
EXPOSE 5173

# Команда по умолчанию — запуск dev-сервера Vite
CMD ["yarn", "dev", "--host"]
