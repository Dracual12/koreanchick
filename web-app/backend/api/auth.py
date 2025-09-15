"""
API эндпоинты для авторизации
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from typing import Dict, Any
import os
from datetime import datetime

from utils.telegram import get_telegram_user_from_request
from utils.database import get_db
from models.user import TelegramUser, UserResponse, UserCreate
from models.base import BaseResponse

router = APIRouter()
security = HTTPBearer()

@router.post("/login", response_model=BaseResponse)
async def login(request: Request, db=Depends(get_db)):
    """
    Авторизация пользователя через Telegram WebApp
    """
    try:
        # Получаем данные пользователя из Telegram
        telegram_user = get_telegram_user_from_request(request)
        
        user_id = telegram_user['id']
        
        # Проверяем, существует ли пользователь в БД
        if not db.check_users_user_exists(user_id):
            # Создаем нового пользователя
            user_link = f"tg://user?id={user_id}"
            reg_time = datetime.utcnow().replace(microsecond=0).isoformat()
            
            db.add_users_user(
                user_id=user_id,
                user_link=user_link,
                user_reg_time=reg_time,
                user_name=telegram_user.get('username'),
                user_first_name=telegram_user.get('first_name'),
                user_last_name=telegram_user.get('last_name')
            )
            
            # Создаем корзину для нового пользователя
            if not db.check_basket_exists(user_id):
                db.create_basket(user_id)
            
            # Устанавливаем дефолтные значения
            db.set_default_q1(user_id)
            db.set_default_q2(user_id)
            
            # Начинаем новую сессию логирования
            db.start_logging_session(str(user_id))
            
            # Логируем ФИО и телефон если есть
            fio = f"{telegram_user.get('first_name', '')} {telegram_user.get('last_name', '')}".strip()
            if fio:
                db.update_logging_session_fio(str(user_id), fio)
        
        # Получаем данные пользователя из БД
        user_data = db.get_users_user(user_id)
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Проверяем, не забанен ли пользователь
        if db.get_users_ban(user_id):
            raise HTTPException(status_code=403, detail="User is banned")
        
        return BaseResponse(
            success=True,
            message="Login successful",
            data={
                "user": {
                    "id": user_data[0],
                    "user_id": user_data[1],
                    "first_name": user_data[4],
                    "last_name": user_data[5],
                    "username": user_data[3],
                    "foodToMoodCoin": user_data[14],
                    "is_banned": bool(user_data[11])
                },
                "telegram_user": telegram_user
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.get("/me", response_model=BaseResponse)
async def get_current_user(request: Request, db=Depends(get_db)):
    """
    Получение данных текущего пользователя
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        if not db.check_users_user_exists(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = db.get_users_user(user_id)
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        return BaseResponse(
            success=True,
            data={
                "user": {
                    "id": user_data[0],
                    "user_id": user_data[1],
                    "first_name": user_data[4],
                    "last_name": user_data[5],
                    "username": user_data[3],
                    "foodToMoodCoin": user_data[14],
                    "is_banned": bool(user_data[11])
                },
                "telegram_user": telegram_user
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user data: {str(e)}")

@router.post("/logout", response_model=BaseResponse)
async def logout(request: Request):
    """
    Выход из системы (в Telegram WebApp это не критично, но для полноты API)
    """
    return BaseResponse(
        success=True,
        message="Logout successful"
    )

@router.get("/verify", response_model=BaseResponse)
async def verify_token(request: Request, db=Depends(get_db)):
    """
    Проверка валидности токена/данных пользователя
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        if not db.check_users_user_exists(user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        if db.get_users_ban(user_id):
            raise HTTPException(status_code=403, detail="User is banned")
        
        return BaseResponse(
            success=True,
            message="Token is valid",
            data={"user_id": user_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token verification failed: {str(e)}")
