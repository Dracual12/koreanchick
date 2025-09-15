"""
Модели блюд и меню
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class DishBase(BaseModel):
    """Базовая модель блюда"""
    dish_name: str
    dish_description: Optional[str] = None
    dish_price: float
    dish_category: Optional[str] = None
    dish_image: Optional[str] = None
    dish_weight: Optional[str] = None
    dish_calories: Optional[int] = None
    dish_ingredients: Optional[str] = None
    dish_allergens: Optional[str] = None
    is_available: bool = True
    is_stop_list: bool = False

class DishCreate(DishBase):
    """Модель для создания блюда"""
    pass

class DishUpdate(BaseModel):
    """Модель для обновления блюда"""
    dish_name: Optional[str] = None
    dish_description: Optional[str] = None
    dish_price: Optional[float] = None
    dish_category: Optional[str] = None
    dish_image: Optional[str] = None
    dish_weight: Optional[str] = None
    dish_calories: Optional[int] = None
    dish_ingredients: Optional[str] = None
    dish_allergens: Optional[str] = None
    is_available: Optional[bool] = None
    is_stop_list: Optional[bool] = None

class DishResponse(DishBase):
    """Модель ответа с данными блюда"""
    id: int
    rest_name: str
    rest_address: str
    iiko_id: Optional[str] = None

class DishListItem(BaseModel):
    """Модель элемента списка блюд"""
    id: int
    dish_name: str
    dish_price: float
    dish_image: Optional[str] = None
    dish_category: Optional[str] = None
    is_available: bool = True
    is_stop_list: bool = False

class CategoryResponse(BaseModel):
    """Модель категории"""
    name: str
    dishes: List[DishListItem]
    total_count: int

class MenuResponse(BaseModel):
    """Модель меню"""
    categories: List[CategoryResponse]
    total_dishes: int
    available_dishes: int

class DishSearchParams(BaseModel):
    """Параметры поиска блюд"""
    query: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    is_available: Optional[bool] = None
    limit: int = 20
    offset: int = 0

class DishRecommendation(BaseModel):
    """Модель рекомендации блюда"""
    dish: DishResponse
    score: float
    reason: str
    mood_match: Optional[str] = None
    preference_match: Optional[str] = None
