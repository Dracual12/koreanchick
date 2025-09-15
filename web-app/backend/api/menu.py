"""
API эндпоинты для меню и блюд
"""

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from typing import List, Optional, Dict, Any

from utils.telegram import get_telegram_user_from_request
from utils.database import get_db
from models.dish import (
    DishResponse, DishListItem, CategoryResponse, MenuResponse,
    DishSearchParams, DishRecommendation
)
from models.base import BaseResponse, PaginatedResponse

router = APIRouter()

@router.get("/", response_model=BaseResponse)
async def get_menu(
    request: Request,
    db=Depends(get_db),
    category: Optional[str] = Query(None, description="Фильтр по категории")
):
    """
    Получение полного меню или меню по категории
    """
    try:
        # Получаем пользователя (для логирования)
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Получаем все блюда
        if category:
            dishes = db.restaurants_get_dish_by_category(category)
        else:
            dishes = db.restaurants_get_all_dish()
        
        # Группируем блюда по категориям
        categories_dict = {}
        total_dishes = 0
        available_dishes = 0
        
        for dish in dishes:
            dish_category = dish[3] or "Без категории"
            dish_item = DishListItem(
                id=dish[0],
                dish_name=dish[1],
                dish_price=dish[2],
                dish_image=dish[4] if len(dish) > 4 else None,
                dish_category=dish_category,
                is_available=not dish[5] if len(dish) > 5 else True,  # Предполагаем что 5-й элемент - stop_list
                is_stop_list=dish[5] if len(dish) > 5 else False
            )
            
            if dish_category not in categories_dict:
                categories_dict[dish_category] = []
            
            categories_dict[dish_category].append(dish_item)
            total_dishes += 1
            
            if dish_item.is_available and not dish_item.is_stop_list:
                available_dishes += 1
        
        # Формируем ответ
        categories = []
        for category_name, category_dishes in categories_dict.items():
            categories.append(CategoryResponse(
                name=category_name,
                dishes=category_dishes,
                total_count=len(category_dishes)
            ))
        
        menu_response = MenuResponse(
            categories=categories,
            total_dishes=total_dishes,
            available_dishes=available_dishes
        )
        
        return BaseResponse(
            success=True,
            data=menu_response.dict()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get menu: {str(e)}")

@router.get("/categories", response_model=BaseResponse)
async def get_categories(request: Request, db=Depends(get_db)):
    """
    Получение списка всех категорий
    """
    try:
        # Получаем все блюда для извлечения категорий
        dishes = db.restaurants_get_all_dish()
        
        categories = set()
        for dish in dishes:
            category = dish[3] if len(dish) > 3 and dish[3] else "Без категории"
            categories.add(category)
        
        return BaseResponse(
            success=True,
            data=list(categories)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get categories: {str(e)}")

@router.get("/search", response_model=BaseResponse)
async def search_dishes(
    request: Request,
    db=Depends(get_db),
    q: str = Query(..., description="Поисковый запрос"),
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    limit: int = Query(20, ge=1, le=100, description="Количество результатов"),
    offset: int = Query(0, ge=0, description="Смещение")
):
    """
    Поиск блюд по названию
    """
    try:
        # Получаем все блюда
        all_dishes = db.restaurants_get_all_dish()
        
        # Фильтруем по поисковому запросу
        filtered_dishes = []
        query_lower = q.lower()
        
        for dish in all_dishes:
            dish_name = dish[1].lower()
            dish_category = dish[3] if len(dish) > 3 else None
            
            # Проверяем соответствие поисковому запросу
            if query_lower in dish_name:
                # Проверяем фильтр по категории
                if category is None or dish_category == category:
                    filtered_dishes.append(dish)
        
        # Применяем пагинацию
        total = len(filtered_dishes)
        paginated_dishes = filtered_dishes[offset:offset + limit]
        
        # Формируем ответ
        dishes_list = []
        for dish in paginated_dishes:
            dishes_list.append(DishListItem(
                id=dish[0],
                dish_name=dish[1],
                dish_price=dish[2],
                dish_image=dish[4] if len(dish) > 4 else None,
                dish_category=dish[3] if len(dish) > 3 else None,
                is_available=not dish[5] if len(dish) > 5 else True,
                is_stop_list=dish[5] if len(dish) > 5 else False
            ))
        
        paginated_response = PaginatedResponse.create(
            items=dishes_list,
            total=total,
            page=(offset // limit) + 1,
            limit=limit
        )
        
        return BaseResponse(
            success=True,
            data=paginated_response.dict()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@router.get("/dish/{dish_id}", response_model=BaseResponse)
async def get_dish(
    dish_id: int,
    request: Request,
    db=Depends(get_db)
):
    """
    Получение детальной информации о блюде
    """
    try:
        # Получаем блюдо по ID
        dish = db.restaurants_get_dish_by_id(dish_id)
        
        if not dish:
            raise HTTPException(status_code=404, detail="Dish not found")
        
        dish_response = DishResponse(
            id=dish[0],
            dish_name=dish[1],
            dish_price=dish[2],
            dish_category=dish[3] if len(dish) > 3 else None,
            dish_image=dish[4] if len(dish) > 4 else None,
            dish_description=dish[6] if len(dish) > 6 else None,
            dish_weight=dish[7] if len(dish) > 7 else None,
            dish_calories=dish[8] if len(dish) > 8 else None,
            dish_ingredients=dish[9] if len(dish) > 9 else None,
            dish_allergens=dish[10] if len(dish) > 10 else None,
            is_available=not dish[5] if len(dish) > 5 else True,
            is_stop_list=dish[5] if len(dish) > 5 else False,
            rest_name=dish[11] if len(dish) > 11 else "Korean Chick",
            rest_address=dish[12] if len(dish) > 12 else "",
            iiko_id=dish[13] if len(dish) > 13 else None
        )
        
        return BaseResponse(
            success=True,
            data=dish_response.dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dish: {str(e)}")

@router.get("/recommendations", response_model=BaseResponse)
async def get_recommendations(
    request: Request,
    db=Depends(get_db),
    limit: int = Query(5, ge=1, le=20, description="Количество рекомендаций")
):
    """
    Получение персональных рекомендаций блюд
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Получаем предпочтения пользователя
        mood = db.get_temp_users_mood(user_id)
        hungry = db.get_temp_users_hungry(user_id)
        style = db.get_temp_users_style(user_id)
        
        # Получаем все доступные блюда
        all_dishes = db.restaurants_get_all_dish()
        
        # Простая логика рекомендаций (можно улучшить)
        recommendations = []
        for dish in all_dishes[:limit * 2]:  # Берем больше для фильтрации
            if len(dish) > 5 and dish[5]:  # Пропускаем стоп-лист
                continue
                
            # Простой алгоритм рекомендаций
            score = 0.5  # Базовый балл
            
            # Учитываем настроение (упрощенно)
            if mood and mood.lower() in ['хорошее', 'отличное']:
                score += 0.2
            
            # Учитываем голод
            if hungry and hungry.lower() in ['очень голоден', 'голоден']:
                score += 0.1
            
            recommendations.append(DishRecommendation(
                dish=DishResponse(
                    id=dish[0],
                    dish_name=dish[1],
                    dish_price=dish[2],
                    dish_category=dish[3] if len(dish) > 3 else None,
                    dish_image=dish[4] if len(dish) > 4 else None,
                    is_available=True,
                    is_stop_list=dish[5] if len(dish) > 5 else False,
                    rest_name=dish[11] if len(dish) > 11 else "Korean Chick",
                    rest_address=dish[12] if len(dish) > 12 else ""
                ),
                score=score,
                reason=f"Рекомендуем на основе ваших предпочтений",
                mood_match=mood,
                preference_match=style
            ))
        
        # Сортируем по баллу и берем топ
        recommendations.sort(key=lambda x: x.score, reverse=True)
        top_recommendations = recommendations[:limit]
        
        return BaseResponse(
            success=True,
            data=[rec.dict() for rec in top_recommendations]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")
