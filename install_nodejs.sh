#!/bin/bash

# Установка Node.js на macOS для Korean Chick

echo "🍗 Установка Node.js для Korean Chick..."

# Проверяем, есть ли уже Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js уже установлен:"
    node -v
    npm -v
    echo ""
    echo "Если версия Node.js меньше 16, рекомендуется обновить."
    echo "Продолжить установку? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Установка отменена."
        exit 0
    fi
fi

# Проверяем, есть ли Homebrew
if ! command -v brew &> /dev/null; then
    echo "📦 Установка Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Добавляем Homebrew в PATH
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
else
    echo "✅ Homebrew уже установлен"
fi

# Устанавливаем Node.js через Homebrew
echo "📦 Установка Node.js..."
brew install node

# Проверяем установку
echo ""
echo "✅ Проверка установки:"
echo "Node.js версия: $(node -v)"
echo "npm версия: $(npm -v)"

echo ""
echo "🎉 Node.js успешно установлен!"
echo ""
echo "Теперь можно запустить:"
echo "  ./start_all.sh  - запустить все сервисы"
echo "  ./quick_test.sh - проверить готовность"
