#!/bin/bash

set -euo pipefail

echo "🔐 Ручной выпуск SSL (DNS-01) для testdlyavsego.ru"

domain="testdlyavsego.ru"
email="admin@testdlyavsego.ru"

# Информативные проверки DNS
echo "🔎 Текущие DNS записи домена:"
A_RECORD=$(dig +short A "$domain" | head -n1 || true)
AAAA_RECORD=$(dig +short AAAA "$domain" | head -n1 || true)
echo " A:    ${A_RECORD:-<нет>}"
echo " AAAA: ${AAAA_RECORD:-<нет>}"

echo ""
echo "ℹ️  Будет использована проверка DNS-01 — открытый порт 80 не требуется."
[ -n "${AAAA_RECORD:-}" ] && echo "⚠️  У домена есть IPv6 (AAAA). Это не мешает DNS-01, можно ничего не менять."

echo ""
echo "📝 Шаги, которые предстоит выполнить:"
echo "  1) Certbot покажет TXT-запись для _acme-challenge.$domain"
echo "  2) Добавьте её в панели DNS провайдера (тип TXT, имя _acme-challenge, значение — строка из certbot)"
echo "  3) Подождите 2–5 минут, пока обновится DNS"
echo "  4) Нажмите Enter в certbot для продолжения проверки"

echo ""
echo "🚀 Запуск certbot в режиме DNS-01 (ручном)"
# Без --non-interactive, т.к. потребуется вручную добавить TXT и подтвердить
sudo certbot certonly \
  --manual \
  --preferred-challenges dns \
  -d "$domain" \
  --agree-tos \
  -m "$email"

CERT_PATH="/etc/letsencrypt/live/$domain/fullchain.pem"
KEY_PATH="/etc/letsencrypt/live/$domain/privkey.pem"

if [ -f "$CERT_PATH" ] && [ -f "$KEY_PATH" ]; then
  echo ""
  echo "✅ Сертификат успешно выпущен!"
  echo "📁 Путь к сертификату: $CERT_PATH"
  echo "🔑 Путь к приватному ключу: $KEY_PATH"
  echo ""
  echo "👉 Подключите эти файлы в ваш веб-сервер/прокси."
else
  echo ""
  echo "❌ Сертификат не найден. Проверьте вывод certbot выше."
  exit 1
fi 