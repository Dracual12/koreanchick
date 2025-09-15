#!/bin/bash

# Korean Chick - Запуск бота и Web App одновременно

echo "🍗 Запуск Korean Chick Bot + Web App..."

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

echo "✅ Все зависимости найдены"

# Функция для остановки всех процессов
cleanup() {
    echo ""
    echo "🛑 Остановка всех серверов..."
    kill $BOT_PID 2>/dev/null
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Все серверы остановлены"
    exit 0
}

# Обработка сигнала завершения
trap cleanup SIGINT SIGTERM

# 1. Запускаем основной бот
echo "🤖 Запуск Telegram бота..."
cd naim
python3 main.py &
BOT_PID=$!
echo "✅ Бот запущен (PID: $BOT_PID)"

# Ждем немного, чтобы бот запустился
sleep 2

# 2. Запускаем backend Web App
echo "🔧 Запуск backend Web App..."
cd ../web-app/backend

# Создаем виртуальное окружение если его нет
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения для backend..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем зависимости
echo "Установка Python зависимостей..."
pip install -r requirements.txt

# Запускаем backend
echo "🚀 Запуск backend сервера..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "✅ Backend запущен (PID: $BACKEND_PID)"

# Ждем немного, чтобы backend запустился
sleep 3

# 3. Запускаем frontend Web App
echo "📱 Запуск frontend Web App..."
cd ../frontend

# Устанавливаем зависимости
echo "Установка Node.js зависимостей..."
npm install

# Запускаем frontend
echo "🚀 Запуск frontend сервера..."
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend запущен (PID: $FRONTEND_PID)"

echo ""
echo "🎉 Все сервисы запущены!"
echo ""
echo "📱 Telegram Bot: Работает"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/api/docs"
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo "📋 Для развертывания на testdlyavsego.ru:"
echo "   1. Собери frontend: cd web-app/frontend && npm run build"
echo "   2. Загрузи содержимое папки dist на твой домен"
echo "   3. Настрой backend на сервере"
echo ""
echo "Для остановки нажмите Ctrl+C"

# Ждем завершения
wait
