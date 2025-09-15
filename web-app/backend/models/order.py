"""
Модели заказов и корзины
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class CartItem(BaseModel):
    """Модель элемента корзины"""
    dish_id: int
    dish_name: str
    quantity: int
    price: float
    total_price: float
    options: Optional[Dict[str, Any]] = None

class CartResponse(BaseModel):
    """Модель корзины"""
    items: List[CartItem]
    total_items: int
    total_price: float
    is_empty: bool = True

class CartUpdate(BaseModel):
    """Модель для обновления корзины"""
    dish_id: int
    quantity: int
    action: str  # "add", "remove", "set"

class OrderCreate(BaseModel):
    """Модель для создания заказа"""
    table_number: Optional[int] = None
    notes: Optional[str] = None
    payment_method: str = "cash"  # "cash", "card", "qr"

class OrderItem(BaseModel):
    """Модель элемента заказа"""
    dish_id: int
    dish_name: str
    quantity: int
    price: float
    total_price: float

class OrderResponse(BaseModel):
    """Модель ответа с данными заказа"""
    id: int
    user_id: int
    waiter_id: Optional[int] = None
    table_number: Optional[int] = None
    order_time: str
    status: str  # "pending", "confirmed", "preparing", "ready", "completed", "cancelled"
    total_amount: float
    items: List[OrderItem]
    notes: Optional[str] = None
    payment_method: str
    qr_code: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    """Модель для обновления статуса заказа"""
    status: str
    notes: Optional[str] = None

class OrderListResponse(BaseModel):
    """Модель списка заказов"""
    orders: List[OrderResponse]
    total: int
    page: int
    limit: int

class QRCodeResponse(BaseModel):
    """Модель QR-кода"""
    qr_code: str
    order_id: int
    expires_at: str

class OrderStats(BaseModel):
    """Статистика заказов"""
    total_orders: int
    total_revenue: float
    average_order_value: float
    orders_by_status: Dict[str, int]
    popular_dishes: List[Dict[str, Any]]
