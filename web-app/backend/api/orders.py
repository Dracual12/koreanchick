"""
API эндпоинты для заказов
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Dict, Any
import json
import qrcode
import tempfile
import os
from datetime import datetime
from io import BytesIO
import base64

from utils.telegram import get_telegram_user_from_request
from utils.database import get_db
from models.order import (
    OrderCreate, OrderResponse, OrderItem, OrderStatusUpdate,
    OrderListResponse, QRCodeResponse
)
from models.base import BaseResponse

router = APIRouter()

@router.post("/create", response_model=BaseResponse)
async def create_order(
    request: Request,
    order_data: OrderCreate,
    db=Depends(get_db)
):
    """
    Создание нового заказа
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Получаем корзину пользователя
        basket_data = db.get_basket(user_id)
        
        if not basket_data or basket_data == "{}":
            raise HTTPException(status_code=400, detail="Cart is empty")
        
        try:
            basket = json.loads(basket_data) if isinstance(basket_data, str) else basket_data
        except (json.JSONDecodeError, TypeError):
            raise HTTPException(status_code=400, detail="Invalid cart data")
        
        # Формируем элементы заказа
        order_items = []
        total_amount = 0.0
        
        for dish_name, dish_data in basket.items():
            if isinstance(dish_data, list) and len(dish_data) >= 2:
                dish_id = dish_data[0]
                quantity = dish_data[1]
                
                # Получаем информацию о блюде
                dish_info = db.restaurants_get_dish_by_id(dish_id)
                if dish_info:
                    price = dish_info[2]
                    total_item_price = price * quantity
                    
                    order_item = OrderItem(
                        dish_id=dish_id,
                        dish_name=dish_name,
                        quantity=quantity,
                        price=price,
                        total_price=total_item_price
                    )
                    
                    order_items.append(order_item)
                    total_amount += total_item_price
        
        if not order_items:
            raise HTTPException(status_code=400, detail="No valid items in cart")
        
        # Создаем заказ в БД
        order_time = datetime.now().isoformat()
        
        # Добавляем заказ (используем метод из оригинальной БД)
        order_id = db.add_order(
            user_id=user_id,
            table_number=order_data.table_number,
            order_time=order_time,
            total_amount=total_amount
        )
        
        # Генерируем QR-код
        qr_data = f"order_{order_id}_{user_id}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Создаем изображение QR-кода
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Конвертируем в base64
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        # Сохраняем QR-код в БД
        db.set_qr_id(user_id, order_id)
        
        # Очищаем корзину после создания заказа
        db.set_basket(user_id, {})
        
        # Логируем заказ в сессии
        order_composition = ", ".join([f"{item.dish_name} x{item.quantity}" for item in order_items])
        db.update_logging_session_order(str(user_id), order_composition)
        db.update_logging_session_sum(str(user_id), total_amount)
        
        order_response = OrderResponse(
            id=order_id,
            user_id=user_id,
            table_number=order_data.table_number,
            order_time=order_time,
            status="pending",
            total_amount=total_amount,
            items=order_items,
            notes=order_data.notes,
            payment_method=order_data.payment_method,
            qr_code=f"data:image/png;base64,{qr_base64}"
        )
        
        return BaseResponse(
            success=True,
            message="Order created successfully",
            data=order_response.dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create order: {str(e)}")

@router.get("/", response_model=BaseResponse)
async def get_user_orders(
    request: Request,
    db=Depends(get_db),
    limit: int = 20,
    offset: int = 0
):
    """
    Получение списка заказов пользователя
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Получаем заказы пользователя из БД
        orders_data = db.get_user_orders(user_id, limit, offset)
        
        orders = []
        for order_data in orders_data:
            # Получаем элементы заказа
            order_items = []
            if len(order_data) > 4:  # Предполагаем что элементы заказа хранятся в 5-м поле
                try:
                    items_data = json.loads(order_data[4]) if isinstance(order_data[4], str) else order_data[4]
                    for item_data in items_data:
                        order_item = OrderItem(
                            dish_id=item_data.get('dish_id', 0),
                            dish_name=item_data.get('dish_name', ''),
                            quantity=item_data.get('quantity', 1),
                            price=item_data.get('price', 0.0),
                            total_price=item_data.get('total_price', 0.0)
                        )
                        order_items.append(order_item)
                except (json.JSONDecodeError, TypeError):
                    pass
            
            order = OrderResponse(
                id=order_data[0],
                user_id=order_data[1],
                waiter_id=order_data[2] if len(order_data) > 2 else None,
                table_number=order_data[3] if len(order_data) > 3 else None,
                order_time=order_data[5] if len(order_data) > 5 else "",
                status=order_data[6] if len(order_data) > 6 else "pending",
                total_amount=order_data[7] if len(order_data) > 7 else 0.0,
                items=order_items,
                notes=order_data[8] if len(order_data) > 8 else None,
                payment_method=order_data[9] if len(order_data) > 9 else "cash"
            )
            orders.append(order)
        
        return BaseResponse(
            success=True,
            data={
                "orders": [order.dict() for order in orders],
                "total": len(orders)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get orders: {str(e)}")

@router.get("/{order_id}", response_model=BaseResponse)
async def get_order(
    order_id: int,
    request: Request,
    db=Depends(get_db)
):
    """
    Получение детальной информации о заказе
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Получаем заказ
        order_data = db.get_order_by_id(order_id)
        
        if not order_data:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Проверяем, что заказ принадлежит пользователю
        if order_data[1] != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Формируем ответ (аналогично get_user_orders)
        order_items = []
        if len(order_data) > 4:
            try:
                items_data = json.loads(order_data[4]) if isinstance(order_data[4], str) else order_data[4]
                for item_data in items_data:
                    order_item = OrderItem(
                        dish_id=item_data.get('dish_id', 0),
                        dish_name=item_data.get('dish_name', ''),
                        quantity=item_data.get('quantity', 1),
                        price=item_data.get('price', 0.0),
                        total_price=item_data.get('total_price', 0.0)
                    )
                    order_items.append(order_item)
            except (json.JSONDecodeError, TypeError):
                pass
        
        order = OrderResponse(
            id=order_data[0],
            user_id=order_data[1],
            waiter_id=order_data[2] if len(order_data) > 2 else None,
            table_number=order_data[3] if len(order_data) > 3 else None,
            order_time=order_data[5] if len(order_data) > 5 else "",
            status=order_data[6] if len(order_data) > 6 else "pending",
            total_amount=order_data[7] if len(order_data) > 7 else 0.0,
            items=order_items,
            notes=order_data[8] if len(order_data) > 8 else None,
            payment_method=order_data[9] if len(order_data) > 9 else "cash"
        )
        
        return BaseResponse(
            success=True,
            data=order.dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get order: {str(e)}")

@router.post("/{order_id}/status", response_model=BaseResponse)
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    request: Request,
    db=Depends(get_db)
):
    """
    Обновление статуса заказа (для официантов)
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Проверяем, является ли пользователь официантом
        if not db.check_waiter_exists(user_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Получаем заказ
        order_data = db.get_order_by_id(order_id)
        if not order_data:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Обновляем статус заказа
        db.update_order_status(order_id, status_update.status, status_update.notes)
        
        return BaseResponse(
            success=True,
            message="Order status updated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update order status: {str(e)}")

@router.get("/qr/{qr_data}", response_model=BaseResponse)
async def get_order_by_qr(
    qr_data: str,
    request: Request,
    db=Depends(get_db)
):
    """
    Получение заказа по QR-коду (для официантов)
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Проверяем, является ли пользователь официантом
        if not db.check_waiter_exists(user_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Парсим QR-данные
        if not qr_data.startswith("order_"):
            raise HTTPException(status_code=400, detail="Invalid QR code")
        
        parts = qr_data.split("_")
        if len(parts) != 3:
            raise HTTPException(status_code=400, detail="Invalid QR code format")
        
        order_id = int(parts[1])
        client_id = int(parts[2])
        
        # Получаем заказ
        order_data = db.get_order_by_id(order_id)
        if not order_data:
            raise HTTPException(status_code=404, detail="Order not found")
        
        # Проверяем, что заказ принадлежит указанному клиенту
        if order_data[1] != client_id:
            raise HTTPException(status_code=400, detail="Invalid order")
        
        # Формируем ответ (аналогично get_order)
        order_items = []
        if len(order_data) > 4:
            try:
                items_data = json.loads(order_data[4]) if isinstance(order_data[4], str) else order_data[4]
                for item_data in items_data:
                    order_item = OrderItem(
                        dish_id=item_data.get('dish_id', 0),
                        dish_name=item_data.get('dish_name', ''),
                        quantity=item_data.get('quantity', 1),
                        price=item_data.get('price', 0.0),
                        total_price=item_data.get('total_price', 0.0)
                    )
                    order_items.append(order_item)
            except (json.JSONDecodeError, TypeError):
                pass
        
        order = OrderResponse(
            id=order_data[0],
            user_id=order_data[1],
            waiter_id=order_data[2] if len(order_data) > 2 else None,
            table_number=order_data[3] if len(order_data) > 3 else None,
            order_time=order_data[5] if len(order_data) > 5 else "",
            status=order_data[6] if len(order_data) > 6 else "pending",
            total_amount=order_data[7] if len(order_data) > 7 else 0.0,
            items=order_items,
            notes=order_data[8] if len(order_data) > 8 else None,
            payment_method=order_data[9] if len(order_data) > 9 else "cash"
        )
        
        return BaseResponse(
            success=True,
            data=order.dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get order by QR: {str(e)}")
