#!/bin/bash

echo "🧹 Очистка и запуск Korean Chick Web App..."

# Остановка всех процессов
echo "🛑 Остановка всех процессов..."
pkill -f "uvicorn" 2>/dev/null
pkill -f "npm run dev" 2>/dev/null
pkill -f "vite" 2>/dev/null
pkill -f "python3.*main" 2>/dev/null

# Ожидание остановки
sleep 2

# Очистка кэша
echo "�� Очистка кэша..."
rm -rf web-app/frontend/node_modules/.vite
rm -rf web-app/frontend/.vite
rm -rf web-app/frontend/dist

# Проверка портов
echo "🔍 Проверка портов..."
if lsof -i :3000 -i :3001 -i :8000 >/dev/null 2>&1; then
    echo "❌ Порты все еще заняты!"
    exit 1
else
    echo "✅ Порты свободны"
fi

echo ""
echo "🎉 Готово к запуску!"
echo ""
echo "Для запуска используй:"
echo "  ./start_backend.sh    # Backend"
echo "  ./start_frontend.sh   # Frontend"
echo ""
