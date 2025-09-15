"""
API эндпоинты для пользователей
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict, Any

from utils.telegram import get_telegram_user_from_request
from utils.database import get_db
from models.user import UserProfile, UserStats
from models.base import BaseResponse

router = APIRouter()

@router.get("/profile", response_model=BaseResponse)
async def get_user_profile(request: Request, db=Depends(get_db)):
    """
    Получение профиля пользователя
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Получаем данные пользователя из БД
        user_data = db.get_users_user(user_id)
        
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Формируем профиль
        profile = UserProfile(
            id=user_data[0],
            user_id=user_data[1],
            first_name=user_data[4],
            last_name=user_data[5],
            username=user_data[3],
            foodToMoodCoin=user_data[14],
            is_banned=bool(user_data[11]),
            registration_date=user_data[6]
        )
        
        return BaseResponse(
            success=True,
            data=profile.dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user profile: {str(e)}")

@router.get("/stats", response_model=BaseResponse)
async def get_user_stats(request: Request, db=Depends(get_db)):
    """
    Получение статистики пользователя
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Получаем статистику заказов
        orders = db.get_user_orders(user_id)
        
        total_orders = len(orders)
        total_spent = sum(order[7] if len(order) > 7 else 0 for order in orders)
        average_order_value = total_spent / total_orders if total_orders > 0 else 0
        
        # Получаем популярные блюда
        popular_dishes = []
        dish_counts = {}
        
        for order in orders:
            if len(order) > 4:
                try:
                    import json
                    items_data = json.loads(order[4]) if isinstance(order[4], str) else order[4]
                    for item_data in items_data:
                        dish_name = item_data.get('dish_name', '')
                        if dish_name:
                            dish_counts[dish_name] = dish_counts.get(dish_name, 0) + 1
                except (json.JSONDecodeError, TypeError):
                    pass
        
        # Сортируем по популярности
        popular_dishes = sorted(dish_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Получаем дату последнего заказа
        last_order_date = None
        if orders:
            last_order = max(orders, key=lambda x: x[5] if len(x) > 5 else "")
            last_order_date = last_order[5] if len(last_order) > 5 else None
        
        stats = UserStats(
            total_orders=total_orders,
            total_spent=total_spent,
            average_order_value=average_order_value,
            favorite_dishes=[dish[0] for dish in popular_dishes],
            last_order_date=last_order_date
        )
        
        return BaseResponse(
            success=True,
            data=stats.dict()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user stats: {str(e)}")

@router.post("/mood", response_model=BaseResponse)
async def update_user_mood(
    request: Request,
    mood_data: Dict[str, Any],
    db=Depends(get_db)
):
    """
    Обновление настроения пользователя
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        mood = mood_data.get('mood')
        if not mood:
            raise HTTPException(status_code=400, detail="Mood is required")
        
        # Обновляем настроение в БД
        db.set_temp_users_mood(user_id, mood)
        
        return BaseResponse(
            success=True,
            message="Mood updated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update mood: {str(e)}")

@router.post("/preferences", response_model=BaseResponse)
async def update_user_preferences(
    request: Request,
    preferences_data: Dict[str, Any],
    db=Depends(get_db)
):
    """
    Обновление предпочтений пользователя
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Обновляем различные предпочтения
        if 'hungry' in preferences_data:
            db.set_temp_users_hungry(user_id, preferences_data['hungry'])
        
        if 'style' in preferences_data:
            db.set_temp_users_style(user_id, preferences_data['style'])
        
        if 'sex' in preferences_data:
            db.set_temp_users_sex(user_id, preferences_data['sex'])
        
        if 'age' in preferences_data:
            db.set_temp_users_age(user_id, preferences_data['age'])
        
        if 'dish_style' in preferences_data:
            db.set_temp_users_dish_style(user_id, preferences_data['dish_style'])
        
        if 'ccal' in preferences_data:
            db.set_temp_users_ccal(user_id, preferences_data['ccal'])
        
        if 'dislike' in preferences_data:
            db.set_temp_users_dislike(user_id, preferences_data['dislike'])
        
        if 'like' in preferences_data:
            db.set_temp_users_like(user_id, preferences_data['like'])
        
        return BaseResponse(
            success=True,
            message="Preferences updated successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update preferences: {str(e)}")

@router.get("/preferences", response_model=BaseResponse)
async def get_user_preferences(request: Request, db=Depends(get_db)):
    """
    Получение предпочтений пользователя
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Получаем все предпочтения
        preferences = {
            'mood': db.get_temp_users_mood(user_id),
            'hungry': db.get_temp_users_hungry(user_id),
            'style': db.get_temp_users_style(user_id),
            'sex': db.get_temp_users_sex(user_id),
            'age': db.get_temp_users_age(user_id),
            'dish_style': db.get_temp_users_dish_style(user_id),
            'ccal': db.get_temp_users_ccal(user_id),
            'dislike': db.get_temp_users_dislike(user_id),
            'like': db.get_temp_users_like(user_id)
        }
        
        return BaseResponse(
            success=True,
            data=preferences
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get preferences: {str(e)}")
