#!/bin/bash

# Korean Chick - Запуск с туннелированием для тестирования в Telegram

echo "🌐 Запуск Korean Chick с туннелированием через testdlyavsego.ru..."

# Функция для остановки всех процессов
cleanup() {
    echo ""
    echo "🛑 Остановка всех серверов и туннелей..."
    kill $BOT_PID 2>/dev/null
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    pkill -f "ngrok http 8000" 2>/dev/null
    pkill -f "ngrok http 3000" 2>/dev/null
    echo "✅ Все серверы и туннели остановлены"
    exit 0
}

# Обработка сигнала завершения
trap cleanup SIGINT SIGTERM

# 1. Запускаем туннели
echo "🌐 Запуск туннелей ngrok..."
ngrok http 8000 --domain=testdlyavsego.ru > /dev/null 2>&1 &
sleep 2
ngrok http 3000 --domain=testdlyavsego.ru > /dev/null 2>&1 &
sleep 2

echo "✅ Туннели запущены"

# 2. Запускаем основной бот
echo "🤖 Запуск Telegram бота..."
cd naim
python3 main.py &
BOT_PID=$!
echo "✅ Бот запущен (PID: $BOT_PID)"

# Ждем немного, чтобы бот запустился
sleep 2

# 3. Запускаем backend Web App
echo "🔧 Запуск backend Web App..."
cd ../web-app/backend

# Активируем виртуальное окружение
source venv/bin/activate

# Запускаем backend
echo "🚀 Запуск backend сервера..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "✅ Backend запущен (PID: $BACKEND_PID)"

# Ждем немного, чтобы backend запустился
sleep 3

# 4. Запускаем frontend Web App
echo "📱 Запуск frontend Web App..."
cd ../frontend

# Запускаем frontend
echo "🚀 Запуск frontend сервера..."
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend запущен (PID: $FRONTEND_PID)"

echo ""
echo "🎉 Все сервисы запущены с туннелированием!"
echo ""
echo "📱 Telegram Bot: Работает"
echo "🔧 Backend API: https://testdlyavsego.ru/api"
echo "📚 API Docs: https://testdlyavsego.ru/api/docs"
echo "🌐 Frontend: https://testdlyavsego.ru"
echo ""
echo "🌐 Туннели ngrok:"
echo "   - Backend: https://testdlyavsego.ru → localhost:8000"
echo "   - Frontend: https://testdlyavsego.ru → localhost:3000"
echo ""
echo "📱 Теперь можно тестировать mini app в Telegram!"
echo "   Откройте бота и нажмите кнопку '🌐 Веб-приложение'"
echo ""
echo "Для остановки нажмите Ctrl+C"

# Ждем завершения
wait
