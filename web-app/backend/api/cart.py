"""
API эндпоинты для корзины
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Dict, Any
import json

from utils.telegram import get_telegram_user_from_request
from utils.database import get_db
from models.order import CartResponse, CartItem, CartUpdate
from models.base import BaseResponse

router = APIRouter()

@router.get("/", response_model=BaseResponse)
async def get_cart(request: Request, db=Depends(get_db)):
    """
    Получение содержимого корзины
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Получаем корзину пользователя
        basket_data = db.get_basket(user_id)
        
        if not basket_data or basket_data == "{}":
            return BaseResponse(
                success=True,
                data=CartResponse(
                    items=[],
                    total_items=0,
                    total_price=0.0,
                    is_empty=True
                ).dict()
            )
        
        # Парсим JSON корзины
        try:
            basket = json.loads(basket_data) if isinstance(basket_data, str) else basket_data
        except (json.JSONDecodeError, TypeError):
            basket = {}
        
        # Формируем список элементов корзины
        cart_items = []
        total_price = 0.0
        
        for dish_name, dish_data in basket.items():
            if isinstance(dish_data, list) and len(dish_data) >= 2:
                dish_id = dish_data[0]
                quantity = dish_data[1]
                
                # Получаем информацию о блюде
                dish_info = db.restaurants_get_dish_by_id(dish_id)
                if dish_info:
                    price = dish_info[2]  # Цена блюда
                    total_item_price = price * quantity
                    
                    cart_item = CartItem(
                        dish_id=dish_id,
                        dish_name=dish_name,
                        quantity=quantity,
                        price=price,
                        total_price=total_item_price
                    )
                    
                    cart_items.append(cart_item)
                    total_price += total_item_price
        
        cart_response = CartResponse(
            items=cart_items,
            total_items=sum(item.quantity for item in cart_items),
            total_price=total_price,
            is_empty=len(cart_items) == 0
        )
        
        return BaseResponse(
            success=True,
            data=cart_response.dict()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get cart: {str(e)}")

@router.post("/add", response_model=BaseResponse)
async def add_to_cart(
    request: Request,
    cart_update: CartUpdate,
    db=Depends(get_db)
):
    """
    Добавление блюда в корзину
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Проверяем существование блюда
        dish_info = db.restaurants_get_dish_by_id(cart_update.dish_id)
        if not dish_info:
            raise HTTPException(status_code=404, detail="Dish not found")
        
        # Проверяем, не в стоп-листе ли блюдо
        if len(dish_info) > 5 and dish_info[5]:  # Предполагаем что 5-й элемент - stop_list
            raise HTTPException(status_code=400, detail="Dish is not available")
        
        # Получаем текущую корзину
        basket_data = db.get_basket(user_id)
        try:
            basket = json.loads(basket_data) if isinstance(basket_data, str) else basket_data
        except (json.JSONDecodeError, TypeError):
            basket = {}
        
        dish_name = dish_info[1]
        
        # Обновляем корзину
        if cart_update.action == "add":
            if dish_name in basket:
                # Увеличиваем количество
                current_quantity = basket[dish_name][1] if isinstance(basket[dish_name], list) else 1
                basket[dish_name] = [cart_update.dish_id, current_quantity + cart_update.quantity]
            else:
                # Добавляем новое блюдо
                basket[dish_name] = [cart_update.dish_id, cart_update.quantity]
        
        elif cart_update.action == "set":
            # Устанавливаем точное количество
            if cart_update.quantity <= 0:
                # Удаляем блюдо из корзины
                basket.pop(dish_name, None)
            else:
                basket[dish_name] = [cart_update.dish_id, cart_update.quantity]
        
        elif cart_update.action == "remove":
            if dish_name in basket:
                current_quantity = basket[dish_name][1] if isinstance(basket[dish_name], list) else 1
                new_quantity = max(0, current_quantity - cart_update.quantity)
                if new_quantity <= 0:
                    basket.pop(dish_name, None)
                else:
                    basket[dish_name] = [cart_update.dish_id, new_quantity]
        
        # Сохраняем обновленную корзину
        db.set_basket(user_id, basket)
        
        return BaseResponse(
            success=True,
            message="Cart updated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update cart: {str(e)}")

@router.delete("/item/{dish_id}", response_model=BaseResponse)
async def remove_from_cart(
    dish_id: int,
    request: Request,
    db=Depends(get_db)
):
    """
    Удаление блюда из корзины
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Получаем текущую корзину
        basket_data = db.get_basket(user_id)
        try:
            basket = json.loads(basket_data) if isinstance(basket_data, str) else basket_data
        except (json.JSONDecodeError, TypeError):
            basket = {}
        
        # Находим и удаляем блюдо
        dish_to_remove = None
        for dish_name, dish_data in basket.items():
            if isinstance(dish_data, list) and len(dish_data) >= 1 and dish_data[0] == dish_id:
                dish_to_remove = dish_name
                break
        
        if dish_to_remove:
            basket.pop(dish_to_remove)
            db.set_basket(user_id, basket)
        
        return BaseResponse(
            success=True,
            message="Item removed from cart"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove item from cart: {str(e)}")

@router.delete("/clear", response_model=BaseResponse)
async def clear_cart(request: Request, db=Depends(get_db)):
    """
    Очистка корзины
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Очищаем корзину
        db.set_basket(user_id, {})
        
        return BaseResponse(
            success=True,
            message="Cart cleared successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear cart: {str(e)}")

@router.get("/count", response_model=BaseResponse)
async def get_cart_count(request: Request, db=Depends(get_db)):
    """
    Получение количества товаров в корзине
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Получаем корзину
        basket_data = db.get_basket(user_id)
        
        if not basket_data or basket_data == "{}":
            return BaseResponse(
                success=True,
                data={"count": 0}
            )
        
        try:
            basket = json.loads(basket_data) if isinstance(basket_data, str) else basket_data
        except (json.JSONDecodeError, TypeError):
            basket = {}
        
        total_count = 0
        for dish_name, dish_data in basket.items():
            if isinstance(dish_data, list) and len(dish_data) >= 2:
                total_count += dish_data[1]
        
        return BaseResponse(
            success=True,
            data={"count": total_count}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get cart count: {str(e)}")
