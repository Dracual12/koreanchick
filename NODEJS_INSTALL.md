# 📦 Установка Node.js для Korean Chick

## 🚀 Быстрая установка:

```bash
./install_nodejs.sh
```

Этот скрипт автоматически:
- ✅ Установит Homebrew (если нужно)
- ✅ Установит Node.js через Homebrew
- ✅ Проверит установку

## 🔧 Ручная установка:

### Вариант 1: Через Homebrew (рекомендуется)
```bash
# Установить Homebrew (если нет)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установить Node.js
brew install node

# Проверить установку
node -v
npm -v
```

### Вариант 2: С официального сайта
1. Перейди на https://nodejs.org
2. Скачай LTS версию для macOS
3. Запусти установщик .pkg
4. Следуй инструкциям

## ✅ Проверка установки:

```bash
node -v    # Должно показать версию Node.js
npm -v     # Должно показать версию npm
```

## 🎯 После установки:

### Запуск всех сервисов:
```bash
./start_all.sh
```

### Проверка готовности:
```bash
./quick_test.sh
```

## 🆘 Решение проблем:

### Если Node.js не найден:
- Перезапусти терминал
- Проверь PATH: `echo $PATH`
- Убедись, что Homebrew в PATH

### Если ошибки прав доступа:
- Не используй `sudo` для npm
- Homebrew устанавливает без sudo

### Если старая версия:
- Обнови через Homebrew: `brew upgrade node`
- Или переустанови: `brew reinstall node`

---

**Готово!** После установки Node.js можно запускать Web App! 🎉
