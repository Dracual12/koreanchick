"""
API эндпоинты для администраторов
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Dict, Any
import os

from utils.telegram import get_telegram_user_from_request
from utils.database import get_db
from models.base import BaseResponse

router = APIRouter()

def check_admin_permissions(user_id: int) -> bool:
    """Проверка прав администратора"""
    admin_ids = os.getenv('ADMIN_USER_IDS', '1456241115').split(',')
    return str(user_id) in admin_ids

@router.get("/stats", response_model=BaseResponse)
async def get_admin_stats(request: Request, db=Depends(get_db)):
    """
    Получение общей статистики для администратора
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Проверяем права администратора
        if not check_admin_permissions(user_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Получаем статистику
        total_users = len(db.get_all_users())
        total_orders = len(db.get_all_orders())
        total_revenue = sum(order[7] if len(order) > 7 else 0 for order in db.get_all_orders())
        
        # Статистика по дням (последние 7 дней)
        recent_orders = db.get_recent_orders(days=7)
        daily_stats = {}
        for order in recent_orders:
            order_date = order[5][:10] if len(order) > 5 else ""  # Берем только дату
            if order_date not in daily_stats:
                daily_stats[order_date] = {'orders': 0, 'revenue': 0}
            daily_stats[order_date]['orders'] += 1
            daily_stats[order_date]['revenue'] += order[7] if len(order) > 7 else 0
        
        # Популярные блюда
        popular_dishes = {}
        for order in db.get_all_orders():
            if len(order) > 4:
                try:
                    import json
                    items_data = json.loads(order[4]) if isinstance(order[4], str) else order[4]
                    for item_data in items_data:
                        dish_name = item_data.get('dish_name', '')
                        if dish_name:
                            popular_dishes[dish_name] = popular_dishes.get(dish_name, 0) + 1
                except (json.JSONDecodeError, TypeError):
                    pass
        
        top_dishes = sorted(popular_dishes.items(), key=lambda x: x[1], reverse=True)[:10]
        
        stats = {
            'total_users': total_users,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'average_order_value': total_revenue / total_orders if total_orders > 0 else 0,
            'daily_stats': daily_stats,
            'popular_dishes': top_dishes
        }
        
        return BaseResponse(
            success=True,
            data=stats
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get admin stats: {str(e)}")

@router.get("/users", response_model=BaseResponse)
async def get_all_users(
    request: Request,
    db=Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """
    Получение списка всех пользователей
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Проверяем права администратора
        if not check_admin_permissions(user_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Получаем пользователей
        all_users = db.get_all_users()
        paginated_users = all_users[offset:offset + limit]
        
        users_data = []
        for user in paginated_users:
            users_data.append({
                'id': user[0],
                'user_id': user[1],
                'first_name': user[4],
                'last_name': user[5],
                'username': user[3],
                'registration_date': user[6],
                'is_banned': bool(user[11]),
                'foodToMoodCoin': user[14]
            })
        
        return BaseResponse(
            success=True,
            data={
                'users': users_data,
                'total': len(all_users),
                'page': (offset // limit) + 1,
                'limit': limit
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get users: {str(e)}")

@router.get("/orders", response_model=BaseResponse)
async def get_all_orders(
    request: Request,
    db=Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """
    Получение списка всех заказов
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Проверяем права администратора
        if not check_admin_permissions(user_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Получаем заказы
        all_orders = db.get_all_orders()
        paginated_orders = all_orders[offset:offset + limit]
        
        orders_data = []
        for order in paginated_orders:
            orders_data.append({
                'id': order[0],
                'user_id': order[1],
                'waiter_id': order[2] if len(order) > 2 else None,
                'table_number': order[3] if len(order) > 3 else None,
                'order_time': order[5] if len(order) > 5 else "",
                'status': order[6] if len(order) > 6 else "pending",
                'total_amount': order[7] if len(order) > 7 else 0.0,
                'notes': order[8] if len(order) > 8 else None,
                'payment_method': order[9] if len(order) > 9 else "cash"
            })
        
        return BaseResponse(
            success=True,
            data={
                'orders': orders_data,
                'total': len(all_orders),
                'page': (offset // limit) + 1,
                'limit': limit
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get orders: {str(e)}")

@router.post("/users/{user_id}/ban", response_model=BaseResponse)
async def ban_user(
    user_id: int,
    request: Request,
    ban_data: Dict[str, Any],
    db=Depends(get_db)
):
    """
    Блокировка/разблокировка пользователя
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        admin_id = telegram_user['id']
        
        # Проверяем права администратора
        if not check_admin_permissions(admin_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        ban_status = ban_data.get('ban', 1)
        
        # Обновляем статус блокировки
        db.set_users_ban(user_id, ban_status)
        
        action = "banned" if ban_status else "unbanned"
        
        return BaseResponse(
            success=True,
            message=f"User {action} successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user ban status: {str(e)}")

@router.get("/stop-list", response_model=BaseResponse)
async def get_stop_list(request: Request, db=Depends(get_db)):
    """
    Получение стоп-листа
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Проверяем права администратора
        if not check_admin_permissions(user_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Получаем блюда в стоп-листе
        all_dishes = db.restaurants_get_all_dish()
        stop_list = []
        
        for dish in all_dishes:
            if len(dish) > 5 and dish[5]:  # Предполагаем что 5-й элемент - stop_list
                stop_list.append({
                    'id': dish[0],
                    'dish_name': dish[1],
                    'dish_price': dish[2],
                    'dish_category': dish[3] if len(dish) > 3 else None
                })
        
        return BaseResponse(
            success=True,
            data=stop_list
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stop list: {str(e)}")

@router.post("/stop-list/{dish_id}", response_model=BaseResponse)
async def update_stop_list(
    dish_id: int,
    request: Request,
    stop_data: Dict[str, Any],
    db=Depends(get_db)
):
    """
    Обновление стоп-листа
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Проверяем права администратора
        if not check_admin_permissions(user_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        is_stop_list = stop_data.get('is_stop_list', False)
        
        # Обновляем статус стоп-листа
        db.update_dish_stop_list(dish_id, is_stop_list)
        
        action = "added to" if is_stop_list else "removed from"
        
        return BaseResponse(
            success=True,
            message=f"Dish {action} stop list successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update stop list: {str(e)}")

@router.get("/export", response_model=BaseResponse)
async def export_data(request: Request, db=Depends(get_db)):
    """
    Экспорт данных (аналогично send_table из основного бота)
    """
    try:
        telegram_user = get_telegram_user_from_request(request)
        user_id = telegram_user['id']
        
        # Проверяем права администратора
        if not check_admin_permissions(user_id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Здесь можно реализовать экспорт данных в Excel
        # Пока возвращаем базовую информацию
        
        export_data = {
            'users_count': len(db.get_all_users()),
            'orders_count': len(db.get_all_orders()),
            'dishes_count': len(db.restaurants_get_all_dish()),
            'export_time': str(datetime.now())
        }
        
        return BaseResponse(
            success=True,
            message="Export data prepared",
            data=export_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export data: {str(e)}")
