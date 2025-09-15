# 🔐 Настройка SSL сертификата для testdlyavsego.ru

## Шаг 1: Настройка DNS записей в reg.ru

1. Зайдите в панель управления reg.ru
2. Перейдите в раздел "Домены" → "Управление DNS"
3. Найдите домен `testdlyavsego.ru`
4. Измените A-запись с `31.31.197.14` на `46.138.179.68`
5. Сохраните изменения
6. Подождите 5-10 минут для распространения DNS

## Шаг 2: Выпуск SSL сертификата

```bash
./setup_ssl.sh
```

Этот скрипт:
- Проверит DNS записи
- Выпустит SSL сертификат через Let's Encrypt
- Сохранит сертификат в `/etc/letsencrypt/live/testdlyavsego.ru/`

## Шаг 3: Настройка nginx с SSL

```bash
./setup_nginx_ssl.sh
```

Этот скрипт:
- Установит nginx (если не установлен)
- Настроит конфигурацию с SSL
- Настроит проксирование на ваши локальные сервисы

## Шаг 4: Запуск сервисов

После настройки SSL запустите ваши сервисы:

```bash
# Backend
cd web-app/backend && source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 &

# Frontend  
cd web-app/frontend && npm run dev &

# Bot
cd naim && python3 main.py &
```

## Шаг 5: Проверка

- Откройте https://testdlyavsego.ru в браузере
- Проверьте, что SSL сертификат работает
- Протестируйте mini app в Telegram

## Автоматическое обновление сертификата

Let's Encrypt сертификаты действительны 90 дней. Для автоматического обновления:

```bash
# Добавьте в crontab
sudo crontab -e

# Добавьте строку:
0 12 * * * /opt/homebrew/bin/certbot renew --quiet
```

## Устранение проблем

### Если DNS не обновился:
- Подождите до 24 часов
- Проверьте: `nslookup testdlyavsego.ru`

### Если сертификат не выпускается:
- Убедитесь, что порты 80 и 443 свободны
- Проверьте, что домен указывает на ваш IP
- Проверьте файрвол

### Если nginx не запускается:
- Проверьте конфигурацию: `sudo nginx -t`
- Проверьте логи: `sudo tail -f /usr/local/var/log/nginx/error.log`
