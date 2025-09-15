"""
Модели пользователей
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TelegramUser(BaseModel):
    """Модель пользователя Telegram"""
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: bool = False
    photo_url: Optional[str] = None

class UserCreate(BaseModel):
    """Модель для создания пользователя"""
    user_id: int
    user_link: str
    user_name: Optional[str] = None
    user_first_name: Optional[str] = None
    user_last_name: Optional[str] = None
    user_reg_time: str
    foodToMoodCoin: int = 0

class UserUpdate(BaseModel):
    """Модель для обновления пользователя"""
    user_first_name: Optional[str] = None
    user_last_name: Optional[str] = None
    user_name: Optional[str] = None
    foodToMoodCoin: Optional[int] = None
    ban: Optional[int] = None

class UserResponse(BaseModel):
    """Модель ответа с данными пользователя"""
    id: int
    user_id: int
    user_link: str
    user_name: Optional[str] = None
    user_first_name: Optional[str] = None
    user_last_name: Optional[str] = None
    user_reg_time: str
    first_message: int = 0
    last_message: int = 0
    mode_id: int = 0
    mode_key: str = ""
    ban: int = 0
    user_verification: Optional[float] = None
    foodToMoodCoin: Optional[int] = None
    last_recomendation_time: Optional[str] = None

class UserProfile(BaseModel):
    """Модель профиля пользователя для фронтенда"""
    id: int
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    foodToMoodCoin: Optional[int] = None
    is_banned: bool = False
    registration_date: str

class UserStats(BaseModel):
    """Статистика пользователя"""
    total_orders: int = 0
    total_spent: float = 0.0
    favorite_dishes: List[str] = []
    last_order_date: Optional[str] = None
