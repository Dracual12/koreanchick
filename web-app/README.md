# Korean Chick Web App

Telegram Mini App для ресторана Korean Chick, полностью повторяющий функционал Telegram бота.

## 🏗️ Архитектура

### Frontend (React + TypeScript)
- **components/ui** - Переиспользуемые UI компоненты
- **components/forms** - Формы для ввода данных
- **components/layout** - Компоненты макета (Header, Sidebar, Footer)
- **pages** - Страницы приложения
- **utils** - Утилиты для работы с данными
- **styles** - Стили и темы
- **assets** - Статические ресурсы

### Backend (FastAPI + Python)
- **api** - API эндпоинты
- **models** - Модели данных (Pydantic)
- **services** - Бизнес-логика
- **utils** - Утилиты и хелперы

### Shared
- **types** - Общие типы TypeScript
- **constants** - Константы приложения
- **utils** - Общие утилиты

## 🚀 Функционал

### Для клиентов:
- 📱 Регистрация и авторизация через Telegram
- 🍽️ Просмотр меню по категориям
- 🛒 Добавление блюд в корзину
- 📝 Заполнение анкеты настроения и предпочтений
- 💳 Оформление заказа с QR-кодом
- ⭐ Оставление отзывов

### Для официантов:
- 📋 Принятие заказов по QR-коду
- 📊 Просмотр статистики заказов
- 💰 Отслеживание заработка

### Для администраторов:
- 🎛️ Управление меню и категориями
- 📈 Просмотр отчетов и статистики
- 👥 Управление официантами
- ⛔ Управление стоп-листом

## 🛠️ Технологии

### Frontend:
- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Zustand (state management)
- React Query (data fetching)

### Backend:
- FastAPI
- SQLite (та же БД что и в боте)
- Pydantic
- Uvicorn

## 📁 Структура файлов

```
web-app/
├── frontend/
│   ├── components/
│   │   ├── ui/           # Button, Input, Modal, etc.
│   │   ├── forms/        # LoginForm, OrderForm, etc.
│   │   └── layout/       # Header, Sidebar, Footer
│   ├── pages/
│   │   ├── auth/         # Login, Register
│   │   ├── menu/         # Menu, Categories, Dish
│   │   ├── cart/         # Cart, Checkout
│   │   ├── profile/      # Profile, Settings
│   │   └── admin/        # Admin panel
│   ├── utils/
│   │   ├── api.ts        # API клиент
│   │   ├── auth.ts       # Авторизация
│   │   └── helpers.ts    # Хелперы
│   ├── styles/
│   │   ├── globals.css
│   │   └── components.css
│   └── assets/
├── backend/
│   ├── api/
│   │   ├── auth.py       # Авторизация
│   │   ├── menu.py       # Меню
│   │   ├── cart.py       # Корзина
│   │   ├── orders.py     # Заказы
│   │   └── admin.py      # Админка
│   ├── models/
│   │   ├── user.py
│   │   ├── dish.py
│   │   ├── order.py
│   │   └── base.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── menu_service.py
│   │   ├── cart_service.py
│   │   └── order_service.py
│   └── utils/
│       ├── database.py   # Подключение к БД
│       └── telegram.py   # Telegram WebApp API
└── shared/
    ├── types/
    │   ├── user.ts
    │   ├── dish.ts
    │   └── order.ts
    ├── constants/
    │   ├── api.ts
    │   └── routes.ts
    └── utils/
        ├── validation.ts
        └── formatting.ts
```

## 🔧 Установка и запуск

### Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend:
```bash
cd frontend
npm install
npm run dev
```

## 📱 Telegram WebApp

Приложение интегрировано с Telegram WebApp API для:
- Авторизации пользователей
- Получения данных профиля
- Отправки уведомлений
- Работы с кнопками и меню

## 🗄️ База данных

Используется та же SQLite база данных что и в основном боте:
- `users` - пользователи
- `baskets` - корзины
- `logging` - логи действий
- `restaurants` - рестораны и блюда
- `orders` - заказы
- `waiters` - официанты

## 🚀 Быстрый старт

### Автоматический запуск (рекомендуется)
```bash
./start.sh
```

### Ручной запуск

#### Backend:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend:
```bash
cd frontend
npm install
npm run dev
```

## 🔧 Настройка

### 1. Настройка переменных окружения

#### Backend (.env):
```env
BOT_TOKEN=your_telegram_bot_token
DATABASE_PATH=../files/databse.db
SECRET_KEY=your_secret_key
ADMIN_USER_IDS=1456241115
```

#### Frontend (.env):
```env
VITE_API_URL=http://localhost:8000/api
VITE_TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

### 2. Настройка Telegram Bot

1. Создайте бота через @BotFather
2. Получите токен бота
3. Добавьте токен в переменные окружения
4. Настройте Web App URL в настройках бота

### 3. Настройка базы данных

Приложение использует ту же SQLite базу данных, что и основной бот. Убедитесь, что путь к базе данных указан правильно в `.env` файле.

## 📱 Использование

### Для пользователей:
1. Откройте приложение в Telegram
2. Авторизуйтесь через Telegram WebApp
3. Просматривайте меню и добавляйте блюда в корзину
4. Оформляйте заказы с QR-кодом

### Для официантов:
1. Войдите в приложение
2. Сканируйте QR-код заказа
3. Подтверждайте заказы
4. Отслеживайте статистику

### Для администраторов:
1. Войдите с правами администратора
2. Просматривайте статистику и отчеты
3. Управляйте меню и пользователями
4. Экспортируйте данные

## 🛠️ Разработка

### Структура проекта:
```
web-app/
├── backend/           # FastAPI сервер
│   ├── api/          # API эндпоинты
│   ├── models/       # Pydantic модели
│   ├── services/     # Бизнес-логика
│   └── utils/        # Утилиты
├── frontend/         # React приложение
│   ├── src/
│   │   ├── components/  # React компоненты
│   │   ├── pages/       # Страницы
│   │   ├── stores/      # Zustand store
│   │   ├── utils/       # Утилиты
│   │   └── types/       # TypeScript типы
└── shared/           # Общие ресурсы
```

### API Endpoints:

#### Авторизация:
- `POST /api/auth/login` - Вход через Telegram
- `GET /api/auth/me` - Получение данных пользователя
- `GET /api/auth/verify` - Проверка токена

#### Меню:
- `GET /api/menu/` - Получение меню
- `GET /api/menu/categories` - Список категорий
- `GET /api/menu/search` - Поиск блюд
- `GET /api/menu/dish/{id}` - Детали блюда
- `GET /api/menu/recommendations` - Рекомендации

#### Корзина:
- `GET /api/cart/` - Получение корзины
- `POST /api/cart/add` - Добавление в корзину
- `DELETE /api/cart/item/{id}` - Удаление из корзины
- `DELETE /api/cart/clear` - Очистка корзины

#### Заказы:
- `POST /api/orders/create` - Создание заказа
- `GET /api/orders/` - Список заказов пользователя
- `GET /api/orders/{id}` - Детали заказа
- `GET /api/orders/qr/{data}` - Заказ по QR-коду

#### Пользователи:
- `GET /api/users/profile` - Профиль пользователя
- `GET /api/users/stats` - Статистика пользователя
- `POST /api/users/preferences` - Обновление предпочтений

#### Админка:
- `GET /api/admin/stats` - Общая статистика
- `GET /api/admin/users` - Список пользователей
- `GET /api/admin/orders` - Все заказы
- `GET /api/admin/export` - Экспорт данных

## 🔒 Безопасность

- Валидация данных через Pydantic
- Проверка Telegram WebApp данных
- CORS настройки для безопасности
- Проверка прав доступа для админки

## 📊 Мониторинг

- Логирование всех операций
- Обработка ошибок
- Валидация входных данных
- Проверка состояния API

## 🚀 Деплой

### Backend (FastAPI):
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск продакшн сервера
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend (React):
```bash
# Сборка для продакшна
npm run build

# Размещение файлов из папки dist на веб-сервере
```

## 🤝 Поддержка

При возникновении проблем:
1. Проверьте логи сервера
2. Убедитесь в правильности настроек
3. Проверьте подключение к базе данных
4. Обратитесь к документации API

## 📝 Лицензия

Проект создан для Korean Chick ресторана.
