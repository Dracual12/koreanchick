#!/bin/bash

# Korean Chick - Развертывание на testdlyavsego.ru

echo "🚀 Развертывание Korean Chick на testdlyavsego.ru..."

# Проверяем наличие Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js не найден. Установите Node.js 16+"
    exit 1
fi

# 1. Собираем frontend для продакшена
echo "📦 Сборка frontend для продакшена..."
cd web-app/frontend

# Устанавливаем зависимости
npm install

# Собираем проект
npm run build

echo "✅ Frontend собран в папку dist/"

# 2. Создаем архив для загрузки
echo "📁 Создание архива для загрузки..."
cd dist
tar -czf ../../../koreanchick-frontend.tar.gz .
cd ../../..

echo "✅ Архив создан: koreanchick-frontend.tar.gz"

# 3. Инструкции по развертыванию
echo ""
echo "📋 Инструкции по развертыванию:"
echo ""
echo "1. 🌐 Frontend (testdlyavsego.ru):"
echo "   - Распакуйте koreanchick-frontend.tar.gz в корень сайта"
echo "   - Убедитесь, что index.html доступен по https://testdlyavsego.ru"
echo ""
echo "2. 🔧 Backend API:"
echo "   - Загрузите папку web-app/backend на сервер"
echo "   - Установите Python 3.8+ и зависимости:"
echo "     cd backend && pip install -r requirements.txt"
echo "   - Запустите: uvicorn main:app --host 0.0.0.0 --port 8000"
echo "   - Настройте проксирование с testdlyavsego.ru/api на localhost:8000"
echo ""
echo "3. 🤖 Telegram Bot:"
echo "   - Загрузите весь проект на сервер"
echo "   - Установите зависимости: pip install -r requirements.txt"
echo "   - Запустите: python3 naim/main.py"
echo ""
echo "4. 🔗 Настройка в @BotFather:"
echo "   - Bot Settings → Menu Button"
echo "   - URL: https://testdlyavsego.ru"
echo "   - Текст: 🌐 Открыть приложение"
echo ""
echo "5. ⚙️ Настройка переменных окружения:"
echo "   - В web-app/backend/.env укажите реальный BOT_TOKEN"
echo "   - В webapp_config.py URL уже настроен на testdlyavsego.ru"
echo ""
echo "🎉 Готово к развертыванию!"
