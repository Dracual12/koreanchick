#!/bin/bash

echo "📱 Запуск Frontend Web App..."

# Переходим в директорию frontend
cd web-app/frontend

# Проверяем, что мы в правильной директории
if [ ! -f "package.json" ]; then
    echo "❌ Ошибка: package.json не найден"
    exit 1
fi

# Устанавливаем зависимости
echo "📦 Установка Node.js зависимостей..."
npm install

# Запускаем frontend
echo "🚀 Запуск frontend сервера..."
echo "📍 Frontend будет доступен по адресу: http://localhost:3000"
echo "⏹️  Для остановки нажмите Ctrl+C"
echo ""

npm run dev
