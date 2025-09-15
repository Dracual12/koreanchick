"""
Базовые модели данных
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class BaseResponse(BaseModel):
    """Базовая модель ответа"""
    success: bool = True
    message: Optional[str] = None
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    """Модель ошибки"""
    success: bool = False
    error: str
    detail: Optional[str] = None

class PaginationParams(BaseModel):
    """Параметры пагинации"""
    page: int = 1
    limit: int = 20
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit

class PaginatedResponse(BaseModel):
    """Пагинированный ответ"""
    items: List[Any]
    total: int
    page: int
    limit: int
    pages: int
    
    @classmethod
    def create(cls, items: List[Any], total: int, page: int, limit: int):
        pages = (total + limit - 1) // limit
        return cls(
            items=items,
            total=total,
            page=page,
            limit=limit,
            pages=pages
        )
