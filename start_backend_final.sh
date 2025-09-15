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

# Проверяем, что все зависимости установлены
echo "📦 Проверка зависимостей..."
python -c "import requests, qrcode; print('✅ Все зависимости установлены')" || {
    echo "❌ Недостающие зависимости, устанавливаем..."
    pip install -r requirements.txt
}

# Запускаем backend БЕЗ reload для стабильности
echo "🚀 Запуск backend сервера..."
echo "📍 Backend будет доступен по адресу: http://localhost:8000"
echo "📚 API документация: http://localhost:8000/docs"
echo "⏹️  Для остановки нажмите Ctrl+C"
echo ""

# Используем полный путь к uvicorn в виртуальном окружении
./venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
