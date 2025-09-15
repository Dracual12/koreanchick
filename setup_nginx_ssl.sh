#!/bin/bash

echo "🌐 Настройка nginx с SSL для testdlyavsego.ru"

# Проверяем, что сертификат существует
if [ ! -f "/etc/letsencrypt/live/testdlyavsego.ru/fullchain.pem" ]; then
    echo "❌ SSL сертификат не найден. Сначала запустите ./setup_ssl.sh"
    exit 1
fi

# Устанавливаем nginx если не установлен
if ! command -v nginx &> /dev/null; then
    echo "📦 Установка nginx..."
    brew install nginx
fi

# Создаем конфигурацию nginx
echo "⚙️ Создание конфигурации nginx..."
sudo tee /usr/local/etc/nginx/sites-available/testdlyavsego.ru > /dev/null << 'NGINX_CONFIG'
server {
    listen 80;
    server_name testdlyavsego.ru;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name testdlyavsego.ru;

    ssl_certificate /etc/letsencrypt/live/testdlyavsego.ru/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/testdlyavsego.ru/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX_CONFIG

# Создаем символическую ссылку
sudo mkdir -p /usr/local/etc/nginx/sites-enabled
sudo ln -sf /usr/local/etc/nginx/sites-available/testdlyavsego.ru /usr/local/etc/nginx/sites-enabled/

# Проверяем конфигурацию
echo "🔍 Проверка конфигурации nginx..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "✅ Конфигурация nginx корректна"
    echo "🚀 Запуск nginx..."
    sudo nginx -s reload
    echo "✅ nginx настроен и запущен с SSL!"
    echo ""
    echo "🌐 Ваш сайт доступен по адресу: https://testdlyavsego.ru"
    echo "📱 Теперь mini app в Telegram будет работать с HTTPS!"
else
    echo "❌ Ошибка в конфигурации nginx"
    exit 1
fi
