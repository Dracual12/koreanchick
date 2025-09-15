#!/bin/bash

# Korean Chick Web App - Скрипт запуска

echo "🍗 Запуск Korean Chick Web App..."

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.8+"
    exit 1
fi

# Проверяем наличие Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js не найден. Установите Node.js 16+"
    exit 1
fi

# Проверяем наличие npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm не найден. Установите npm"
    exit 1
fi

echo "✅ Все зависимости найдены"

# Создаем виртуальное окружение для backend
echo "📦 Настройка backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем зависимости
echo "Установка Python зависимостей..."
pip install -r requirements.txt

# Запускаем backend в фоне
echo "🚀 Запуск backend сервера..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ../frontend

# Устанавливаем зависимости frontend
echo "📦 Настройка frontend..."
npm install

# Запускаем frontend
echo "🚀 Запуск frontend сервера..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 Korean Chick Web App запущен!"
echo ""
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/api/docs"
echo ""
echo "Для остановки нажмите Ctrl+C"

# Функция для остановки процессов
cleanup() {
    echo ""
    echo "🛑 Остановка серверов..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Серверы остановлены"
    exit 0
}

# Обработка сигнала завершения
trap cleanup SIGINT SIGTERM

# Ждем завершения
wait
