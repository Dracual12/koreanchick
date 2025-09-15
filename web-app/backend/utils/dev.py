"""
Утилиты для режима разработки
"""

import os
from typing import Dict, Any

def is_development() -> bool:
    """Проверяет, находимся ли мы в режиме разработки"""
    return os.getenv('ENVIRONMENT', 'development') == 'development'

def get_mock_telegram_user() -> Dict[str, Any]:
    """Возвращает моковые данные пользователя для разработки"""
    return {
        'id': 123456789,
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'testuser',
        'language_code': 'ru',
        'is_premium': False,
        'photo_url': None
    }

def get_mock_init_data() -> str:
    """Возвращает моковые initData для разработки"""
    return 'user=%7B%22id%22%3A123456789%2C%22first_name%22%3A%22Test%22%2C%22last_name%22%3A%22User%22%2C%22username%22%3A%22testuser%22%2C%22language_code%22%3A%22ru%22%2C%22is_premium%22%3Afalse%7D&chat_instance=-123456789&chat_type=sender&auth_date=1234567890&hash=mock_hash'
