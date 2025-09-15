"""
Утилиты для работы с Telegram WebApp API
"""

import hashlib
import hmac
import json
from typing import Dict, Any, Optional
from fastapi import HTTPException, Request
from .dev import is_development, get_mock_telegram_user

class TelegramWebAppValidator:
    """Валидатор для Telegram WebApp данных"""
    
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
    
    def validate_init_data(self, init_data: str) -> Dict[str, Any]:
        """
        Валидирует initData от Telegram WebApp
        
        Args:
            init_data: Строка initData от Telegram
            
        Returns:
            Dict с данными пользователя
            
        Raises:
            HTTPException: Если данные невалидны
        """
        try:
            # В режиме разработки пропускаем валидацию
            if is_development() and init_data == 'mock_data':
                return {
                    'user': get_mock_telegram_user(),
                    'auth_date': '1234567890',
                    'hash': 'mock_hash'
                }
            
            # Парсим данные
            parsed_data = {}
            for item in init_data.split('&'):
                if '=' in item:
                    key, value = item.split('=', 1)
                    parsed_data[key] = value
            
            # Проверяем наличие hash
            if 'hash' not in parsed_data:
                raise HTTPException(status_code=400, detail="Missing hash in init data")
            
            received_hash = parsed_data.pop('hash')
            
            # Создаем строку для проверки
            data_check_string = '&'.join([f"{k}={v}" for k, v in sorted(parsed_data.items())])
            
            # Создаем секретный ключ
            secret_key = hmac.new(
                "WebAppData".encode(),
                self.bot_token.encode(),
                hashlib.sha256
            ).digest()
            
            # Вычисляем hash
            calculated_hash = hmac.new(
                secret_key,
                data_check_string.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Проверяем hash
            if not hmac.compare_digest(received_hash, calculated_hash):
                raise HTTPException(status_code=400, detail="Invalid hash")
            
            # Парсим JSON данные
            if 'user' in parsed_data:
                parsed_data['user'] = json.loads(parsed_data['user'])
            
            return parsed_data
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid init data: {str(e)}")
    
    def extract_user_data(self, init_data: str) -> Dict[str, Any]:
        """
        Извлекает данные пользователя из initData
        
        Args:
            init_data: Строка initData от Telegram
            
        Returns:
            Dict с данными пользователя
        """
        validated_data = self.validate_init_data(init_data)
        
        if 'user' not in validated_data:
            raise HTTPException(status_code=400, detail="No user data in init data")
        
        user_data = validated_data['user']
        
        return {
            'id': user_data.get('id'),
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
            'username': user_data.get('username'),
            'language_code': user_data.get('language_code'),
            'is_premium': user_data.get('is_premium', False),
            'photo_url': user_data.get('photo_url')
        }

def get_telegram_user_from_request(request: Request) -> Dict[str, Any]:
    """
    Извлекает данные пользователя Telegram из заголовков запроса
    
    Args:
        request: FastAPI Request объект
        
    Returns:
        Dict с данными пользователя
    """
    # Получаем initData из заголовков
    init_data = request.headers.get('X-Telegram-Init-Data')
    
    if not init_data:
        # В режиме разработки используем моковые данные
        if is_development():
            return get_mock_telegram_user()
        raise HTTPException(status_code=401, detail="Missing Telegram init data")
    
    # Создаем валидатор (токен бота должен быть в переменных окружения)
    import os
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        # В режиме разработки используем моковый токен
        if is_development():
            bot_token = 'mock_bot_token'
        else:
            raise HTTPException(status_code=500, detail="Bot token not configured")
    
    validator = TelegramWebAppValidator(bot_token)
    return validator.extract_user_data(init_data)
