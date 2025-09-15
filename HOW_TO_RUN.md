# 🚀 Как запустить Korean Chick Bot + Web App

## 📋 Быстрый старт

### 1. 🧪 Проверка готовности
```bash
./quick_test.sh
```
Этот скрипт проверит, что все файлы на месте и конфигурация правильная.

### 2. 🎯 Запуск всего сразу
```bash
./start_all.sh
```
Этот скрипт запустит:
- 🤖 Telegram бота
- 🔧 Backend API (порт 8000)
- 📱 Frontend Web App (порт 3000)

### 3. 🌐 Развертывание на домен
```bash
./deploy.sh
```
Этот скрипт подготовит все для загрузки на `testdlyavsego.ru`

## 🔧 Ручной запуск (если нужно)

### Запуск только бота:
```bash
cd naim
python3 main.py
```

### Запуск только Web App:
```bash
cd web-app
./start.sh
```

### Запуск только backend:
```bash
cd web-app/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Запуск только frontend:
```bash
cd web-app/frontend
npm install
npm run dev
```

## 📱 Что будет работать

### После запуска `./start_all.sh`:

1. **🤖 Telegram Bot** - работает как обычно
   - Отправьте `/start` боту
   - Увидите кнопку "🌐 Веб-приложение"

2. **🌐 Web App** - http://localhost:3000
   - Современный интерфейс
   - Все функции бота в веб-формате

3. **🔧 API** - http://localhost:8000
   - Документация: http://localhost:8000/api/docs
   - Все эндпоинты для Web App

## 🌐 Развертывание на testdlyavsego.ru

### 1. Подготовка:
```bash
./deploy.sh
```

### 2. Загрузка на сервер:
- **Frontend**: Загрузите содержимое `dist/` в корень сайта
- **Backend**: Загрузите папку `web-app/backend/` на сервер
- **Bot**: Загрузите весь проект на сервер

### 3. Настройка сервера:
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

# Bot
python3 naim/main.py
```

### 4. Настройка в Telegram:
- Откройте @BotFather
- Bot Settings → Menu Button
- URL: `https://testdlyavsego.ru`

## ⚙️ Настройка переменных окружения

### В `web-app/backend/.env`:
```env
BOT_TOKEN=ваш_реальный_токен_бота
WEBAPP_URL=https://testdlyavsego.ru
DATABASE_PATH=../files/databse.db
```

### В `web-app/frontend/.env`:
```env
VITE_API_URL=https://testdlyavsego.ru/api
VITE_TELEGRAM_BOT_TOKEN=ваш_реальный_токен_бота
```

## �� Тестирование

### Локальное тестирование:
1. Запустите `./start_all.sh`
2. Откройте http://localhost:3000
3. Отправьте `/start` боту
4. Нажмите кнопку "🌐 Веб-приложение"

### Тестирование на домене:
1. Разверните на `testdlyavsego.ru`
2. Отправьте `/start` боту
3. Нажмите кнопку "🌐 Веб-приложение"
4. Web App должен открыться на твоем домене

## 🆘 Решение проблем

### Бот не запускается:
- Проверьте токен бота в настройках
- Убедитесь, что все зависимости установлены

### Web App не открывается:
- Проверьте, что frontend запущен на порту 3000
- Убедитесь, что backend запущен на порту 8000

### Ошибки в браузере:
- Откройте консоль разработчика (F12)
- Проверьте ошибки в Network и Console

### Проблемы с базой данных:
- Убедитесь, что файл `files/databse.db` существует
- Проверьте права доступа к файлу

## 📞 Поддержка

Если что-то не работает:
1. Запустите `./quick_test.sh` для диагностики
2. Проверьте логи в консоли
3. Убедитесь, что все порты свободны
4. Проверьте настройки файрвола

---

**Готово!** 🎉 Теперь у тебя есть все для запуска и развертывания!
