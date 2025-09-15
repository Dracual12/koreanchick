#!/bin/bash

echo "🛑 Остановка всех процессов Korean Chick..."

# Поиск и остановка всех процессов бота
echo "�� Поиск процессов бота..."
BOT_PIDS=$(ps aux | grep "main.py" | grep -v grep | awk '{print $2}')

if [ -n "$BOT_PIDS" ]; then
    echo "📱 Найдены процессы бота: $BOT_PIDS"
    for pid in $BOT_PIDS; do
        echo "🛑 Остановка процесса $pid..."
        kill $pid
    done
    sleep 2
else
    echo "✅ Процессы бота не найдены"
fi

# Остановка всех других процессов
echo "🛑 Остановка uvicorn..."
pkill -f "uvicorn" 2>/dev/null

echo "🛑 Остановка npm и vite..."
pkill -f "npm run dev" 2>/dev/null
pkill -f "vite" 2>/dev/null

# Ожидание остановки
sleep 2

# Проверка портов
echo "🔍 Проверка портов..."
if lsof -i :3000 -i :3001 -i :8000 >/dev/null 2>&1; then
    echo "❌ Порты все еще заняты!"
    echo "Занятые порты:"
    lsof -i :3000 -i :3001 -i :8000
else
    echo "✅ Все порты свободны"
fi

echo ""
echo "🎉 Все процессы остановлены!"
echo ""
echo "Теперь можешь запускать:"
echo "  ./start_backend.sh    # Backend"
echo "  ./start_frontend.sh   # Frontend"
echo ""
