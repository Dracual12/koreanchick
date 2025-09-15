#!/bin/bash

# Korean Chick - Запуск с Cloudflare Tunnel для тестирования в Telegram

echo "🌐 Запуск Korean Chick с Cloudflare Tunnel..."

# Проверяем наличие cloudflared
if ! command -v cloudflared &> /dev/null; then
    echo "❌ cloudflared не найден. Установите: brew install cloudflared"
    exit 1
fi

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
    kill $TUNNEL_PID 2>/dev/null
    echo "✅ Все серверы остановлены"
    exit 0
}

# Обработка сигнала завершения
trap cleanup SIGINT SIGTERM

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

# Запускаем frontend
npm run dev &
FRONTEND_PID=$!
echo "✅ Frontend запущен (PID: $FRONTEND_PID)"

# Ждем запуска frontend
sleep 5

# 3. Запускаем Cloudflare Tunnel для frontend
echo "🌐 Запуск Cloudflare Tunnel для frontend..."
cloudflared tunnel --url http://localhost:3000 &
TUNNEL_PID=$!
sleep 3

# Получаем URL туннеля (это может занять время)
echo "⏳ Ожидание создания туннеля..."
sleep 5

# Пытаемся получить URL из логов cloudflared
TUNNEL_URL=$(ps aux | grep cloudflared | grep -o 'https://[^[:space:]]*\.trycloudflare\.com' | head -1)

if [ -z "$TUNNEL_URL" ]; then
    echo "⚠️  Не удалось автоматически получить URL туннеля"
    echo "📋 Проверьте вывод cloudflared выше для получения URL"
    echo "🔗 URL должен выглядеть как: https://xxxxx.trycloudflare.com"
    echo ""
    echo "Введите URL туннеля вручную (или нажмите Enter для продолжения):"
    read -r TUNNEL_URL
fi

if [ -n "$TUNNEL_URL" ]; then
    echo "✅ Туннель создан: $TUNNEL_URL"
    
    # Обновляем конфигурацию frontend
    echo "🔧 Обновление конфигурации frontend..."
    cat > .env << EOF_ENV
VITE_API_URL=$TUNNEL_URL/api
EOF_ENV
    
    echo "✅ Frontend настроен на API: $TUNNEL_URL/api"
fi

# 4. Запускаем бота
echo "🤖 Запуск Telegram бота..."
cd ../../naim

# Создаем временный webapp_config с URL туннеля
if [ -n "$TUNNEL_URL" ]; then
    cat > webapp_config_temp.py << EOF_CONFIG
"""
Временная конфигурация для Web App с туннелем
"""

WEBAPP_URL = "$TUNNEL_URL"

def get_webapp_url():
    return WEBAPP_URL
EOF_CONFIG
fi

# Запускаем бота
python3 main.py &
BOT_PID=$!
echo "✅ Бот запущен (PID: $BOT_PID)"

echo ""
echo "🎉 Все сервисы запущены с туннелированием!"
echo ""
if [ -n "$TUNNEL_URL" ]; then
    echo "🌐 Web App URL: $TUNNEL_URL"
    echo "🔧 Backend API: $TUNNEL_URL/api"
else
    echo "🌐 Web App URL: Проверьте вывод cloudflared выше"
fi
echo "📱 Frontend: http://localhost:3000"
echo "🤖 Telegram Bot: Работает"
echo ""
echo "📋 Для тестирования в Telegram:"
echo "   1. Откройте бота в Telegram"
echo "   2. Нажмите кнопку '🌐 Веб-приложение'"
if [ -n "$TUNNEL_URL" ]; then
    echo "   3. Mini app должен открыться по адресу: $TUNNEL_URL"
else
    echo "   3. Mini app откроется по URL из cloudflared"
fi
echo ""
echo "⚠️  ВАЖНО: Не закрывайте этот терминал!"
echo "   Туннель работает только пока запущен cloudflared"
echo ""
echo "Для остановки нажмите Ctrl+C"

# Ждем завершения
wait
