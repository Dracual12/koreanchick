#!/bin/bash

# Korean Chick - Быстрое тестирование

echo "🧪 Быстрое тестирование Korean Chick..."

# Проверяем, что все файлы на месте
echo "📁 Проверка файлов..."

if [ ! -f "naim/main.py" ]; then
    echo "❌ Файл naim/main.py не найден"
    exit 1
fi

if [ ! -f "web-app/backend/main.py" ]; then
    echo "❌ Файл web-app/backend/main.py не найден"
    exit 1
fi

if [ ! -f "web-app/frontend/package.json" ]; then
    echo "❌ Файл web-app/frontend/package.json не найден"
    exit 1
fi

if [ ! -f "webapp_config.py" ]; then
    echo "❌ Файл webapp_config.py не найден"
    exit 1
fi

echo "✅ Все файлы на месте"

# Проверяем конфигурацию
echo "⚙️ Проверка конфигурации..."

if grep -q "testdlyavsego.ru" webapp_config.py; then
    echo "✅ Домен testdlyavsego.ru настроен"
else
    echo "❌ Домен не настроен в webapp_config.py"
fi

if [ -f "web-app/backend/.env" ]; then
    echo "✅ Backend .env файл существует"
else
    echo "⚠️ Backend .env файл не найден (создайте его)"
fi

if [ -f "web-app/frontend/.env" ]; then
    echo "✅ Frontend .env файл существует"
else
    echo "⚠️ Frontend .env файл не найден (создайте его)"
fi

echo ""
echo "🚀 Для запуска используйте:"
echo "   ./start_all.sh  - запустить все сервисы"
echo "   ./deploy.sh     - подготовить к развертыванию"
echo ""
echo "📱 После запуска:"
echo "   - Бот: Отправьте /start в Telegram"
echo "   - Web App: http://localhost:3000"
echo "   - API: http://localhost:8000/api/docs"
echo ""
echo "🌐 Для развертывания на testdlyavsego.ru:"
echo "   1. Запустите ./deploy.sh"
echo "   2. Следуйте инструкциям"
