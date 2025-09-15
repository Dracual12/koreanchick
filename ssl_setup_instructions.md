# Инструкции по настройке SSL для testdlyavsego.ru

## Вариант 1: Если у вас есть доступ к серверу

### На сервере выполните:
```bash
# Установите certbot
sudo apt update
sudo apt install certbot python3-certbot-nginx  # для nginx
# или
sudo apt install certbot python3-certbot-apache  # для apache

# Получите сертификат
sudo certbot --nginx -d testdlyavsego.ru
# или
sudo certbot --apache -d testdlyavsego.ru

# Автоматическое обновление
sudo crontab -e
# Добавьте строку:
0 12 * * * /usr/bin/certbot renew --quiet
```

## Вариант 2: Если нет доступа к серверу

### Используйте DNS challenge:
```bash
# На локальной машине
sudo certbot certonly --manual --preferred-challenges dns -d testdlyavsego.ru

# Certbot покажет TXT запись для добавления в DNS
# Добавьте её в настройки DNS вашего домена
# Затем нажмите Enter
```

## Вариант 3: Через хостинг-провайдера

### Если домен на REG.RU или другом хостинге:
1. Зайдите в панель управления хостингом
2. Найдите раздел "SSL сертификаты" или "Безопасность"
3. Включите "Let's Encrypt" или "Бесплатный SSL"
4. Активируйте для домена testdlyavsego.ru

## Проверка SSL:
```bash
curl -I https://testdlyavsego.ru
openssl s_client -connect testdlyavsego.ru:443 -servername testdlyavsego.ru
```
