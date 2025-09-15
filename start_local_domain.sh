#!/bin/bash

# Korean Chick - Запуск с локальным доменом для тестирования

echo "🌐 Запуск Korean Chick с локальным доменом..."

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден"
    exit 1
fi

# Проверяем наличие Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js не найден"
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

# Получаем локальный IP
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)
LOCAL_DOMAIN="http://$LOCAL_IP:3000"

echo "🌐 Локальный домен: $LOCAL_DOMAIN"

# 1. Запускаем backend
echo "🔧 Запуск backend..."
cd web-app/backend

# Активируем виртуальное окружение
source venv/bin/activate

# Запускаем backend
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "✅ Backend запущен (PID: $BACKEND_PID)"

# Ждем запуска backend
sleep 3

# 2. Запускаем frontend
echo "📱 Запуск frontend..."
cd ../frontend

# Устанавливаем зависимости если нужно
if [ ! -d "node_modules" ]; then
    echo "Установка Node.js зависимостей..."
    npm install
fi

# Настраиваем frontend для использования локального IP
echo "🔧 Настройка frontend для локального IP..."
cat > .env << EOF_ENV
VITE_API_URL=http://$LOCAL_IP:8000/api
EOF_ENV

# Запускаем frontend
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!
echo "✅ Frontend запущен (PID: $FRONTEND_PID)"

# Ждем запуска frontend
sleep 5

# 3. Запускаем бота
echo "🤖 Запуск Telegram бота..."
cd ../../naim

# Создаем временный webapp_config с локальным IP
cat > webapp_config_temp.py << EOF_CONFIG
"""
Временная конфигурация для Web App с локальным IP
"""

WEBAPP_URL = "$LOCAL_DOMAIN"

def get_webapp_url():
    return WEBAPP_URL
EOF_CONFIG

# Запускаем бота
python3 main.py &
BOT_PID=$!
echo "✅ Бот запущен (PID: $BOT_PID)"

echo ""
echo "🎉 Все сервисы запущены!"
echo ""
echo "🌐 Web App URL: $LOCAL_DOMAIN"
echo "🔧 Backend API: http://$LOCAL_IP:8000"
echo "📱 Frontend: http://localhost:3000"
echo "🤖 Telegram Bot: Работает"
echo ""
echo "📋 Для тестирования:"
echo "   1. Откройте бота в Telegram"
echo "   2. Нажмите кнопку '🌐 Веб-приложение'"
echo "   3. Mini app должен открыться по адресу: $LOCAL_DOMAIN"
echo ""
echo "⚠️  ВАЖНО:"
echo "   - Убедитесь что ваш Mac и телефон в одной Wi-Fi сети"
echo "   - Проверьте что порты 3000 и 8000 открыты в файрволе"
echo "   - Если не работает, попробуйте отключить файрвол временно"
echo ""
echo "Для остановки нажмите Ctrl+C"

# Ждем завершения
wait
