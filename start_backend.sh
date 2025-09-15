#!/bin/bash

echo "🔧 Запуск Backend Web App..."

# Переходим в директорию backend
cd web-app/backend

# Проверяем, что мы в правильной директории
if [ ! -f "main.py" ]; then
    echo "❌ Ошибка: main.py не найден"
    exit 1
fi

# Устанавливаем зависимости
echo "📦 Установка зависимостей..."
pip3 install -r requirements.txt

# Запускаем backend
echo "🚀 Запуск backend сервера..."
echo "📍 Backend будет доступен по адресу: http://localhost:8000"
echo "📚 API документация: http://localhost:8000/docs"
echo "⏹️  Для остановки нажмите Ctrl+C"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
