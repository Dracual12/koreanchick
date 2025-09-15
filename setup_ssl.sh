#!/bin/bash

echo "🔐 Настройка SSL сертификата для testdlyavsego.ru"

# Проверяем, что домен указывает на наш IP
echo "🔍 Проверка DNS записей..."
CURRENT_IP=$(curl -4 -s ifconfig.me)
DOMAIN_IP=$(nslookup testdlyavsego.ru | grep "Address:" | tail -1 | awk '{print $2}')

echo "Ваш IP: $CURRENT_IP"
echo "IP домена: $DOMAIN_IP"

if [ "$CURRENT_IP" != "$DOMAIN_IP" ]; then
    echo "❌ Ошибка: Домен testdlyavsego.ru указывает на $DOMAIN_IP, а ваш IP $CURRENT_IP"
    echo "📝 Нужно изменить A-запись в панели reg.ru на $CURRENT_IP"
    echo "⏳ Подождите 5-10 минут после изменения DNS и запустите скрипт снова"
    exit 1
fi

# Доп. проверка IPv6: если есть AAAA-запись и она не совпадает с нашим публичным IPv6 — останавливаемся
DOMAIN_IPV6=$(dig +short AAAA testdlyavsego.ru | head -n1)
CURRENT_IPV6=$(curl -6 -s ifconfig.me)
if [ -n "$DOMAIN_IPV6" ]; then
    echo "IPv6 домена: $DOMAIN_IPV6"
    if [ -z "$CURRENT_IPV6" ]; then
        echo "❌ Обнаружена AAAA-запись $DOMAIN_IPV6, но у этого хоста нет публичного IPv6."
        echo "🛠 Удалите временно AAAA-запись для testdlyavsego.ru или укажите корректный IPv6 этого хоста, затем повторите попытку."
        exit 1
    fi
    if [ "$DOMAIN_IPV6" != "$CURRENT_IPV6" ]; then
        echo "❌ Несовпадение IPv6: домен указывает на $DOMAIN_IPV6, а публичный IPv6 этого хоста $CURRENT_IPV6"
        echo "🛠 Либо исправьте AAAA-запись на $CURRENT_IPV6, либо временно удалите AAAA, чтобы верификация шла по IPv4."
        exit 1
    fi
fi

echo "✅ DNS записи настроены правильно"

# Останавливаем все сервисы на портах 80 и 443
echo "🛑 Остановка сервисов на портах 80 и 443..."
sudo lsof -ti:80 | xargs sudo kill -9 2>/dev/null || true
sudo lsof -ti:443 | xargs sudo kill -9 2>/dev/null || true

# Удалён запуск временного веб-сервера, чтобы certbot --standalone мог занять порт 80
# Запуск временного веб-сервера ранее блокировал порт 80 и мешал certbot

# Выпускаем SSL сертификат
echo "🔐 Выпуск SSL сертификата..."
sudo certbot certonly --standalone --preferred-challenges http --http-01-address 0.0.0.0 --http-01-port 80 -d testdlyavsego.ru --non-interactive --agree-tos --email admin@testdlyavsego.ru

# Проверяем, что сертификат создан
if [ -f "/etc/letsencrypt/live/testdlyavsego.ru/fullchain.pem" ]; then
    echo "✅ SSL сертификат успешно создан!"
    echo "📁 Сертификат находится в: /etc/letsencrypt/live/testdlyavsego.ru/"
    echo ""
    echo "🔧 Для использования сертификата:"
    echo "   - Скопируйте сертификаты в папку проекта"
    echo "   - Настройте nginx/apache для использования HTTPS"
    echo "   - Обновите конфигурацию приложения"
else
    echo "❌ Ошибка при создании SSL сертификата"
    exit 1
fi
