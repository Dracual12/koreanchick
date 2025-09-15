#!/bin/bash

echo "🔧 Запуск Backend Web App..."

# Переходим в директорию backend
cd web-app/backend

# Проверяем, что мы в правильной директории
if [ ! -f "main.py" ]; then
    echo "❌ Ошибка: main.py не найден"
    exit 1
fi

# Активируем виртуальное окружение
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Проверяем, что requests установлен
echo "📦 Проверка зависимостей..."
python -c "import requests; print('✅ requests установлен')" || {
    echo "❌ requests не найден, устанавливаем..."
    pip install requests
}

# Запускаем backend
echo "🚀 Запуск backend сервера..."
echo "📍 Backend будет доступен по адресу: http://localhost:8000"
echo "📚 API документация: http://localhost:8000/docs"
echo "⏹️  Для остановки нажмите Ctrl+C"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
