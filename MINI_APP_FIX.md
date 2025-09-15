# 🔧 Исправление проблемы с Mini App в Telegram

## Проблема
Mini app в Telegram показывает бесконечную загрузку из-за неправильной конфигурации API URL.

## Причина
- Бот настроен на URL `https://testdlyavsego.ru`
- Frontend пытается подключиться к API на `http://localhost:8000`
- localhost недоступен из интернета, поэтому API запросы не проходят

## Решение

### 1. ✅ Исправлено: Добавлены файлы окружения
Созданы файлы `.env` и `.env.production` в `web-app/frontend/` с правильным API URL:
```
VITE_API_URL=https://testdlyavsego.ru/api
```

### 2. 🔧 Нужно сделать: Развертывание на сервере

#### Frontend:
```bash
cd web-app/frontend
npm run build
# Загрузить содержимое папки dist на testdlyavsego.ru
```

#### Backend:
```bash
# На сервере testdlyavsego.ru:
cd web-app/backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Настройка проксирования:
Нужно настроить nginx/apache чтобы:
- `https://testdlyavsego.ru/api/*` → `http://localhost:8000/api/*`
- `https://testdlyavsego.ru/*` → статические файлы frontend

### 3. 🚀 Использование исправленных скриптов

#### Для локальной разработки:
```bash
./start_all_fixed.sh
```

#### Для production деплоя:
```bash
./deploy.sh
```

## Проверка
После развертывания:
1. Откройте https://testdlyavsego.ru в браузере
2. Проверьте что API работает: https://testdlyavsego.ru/api/health
3. Протестируйте mini app в Telegram боте

## Важно
- Локально mini app работает только в браузере на localhost:3000
- В Telegram mini app работает только после деплоя на testdlyavsego.ru
- Всегда используйте `./start_all_fixed.sh` для запуска
