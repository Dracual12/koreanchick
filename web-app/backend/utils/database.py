"""
Менеджер базы данных для Web App
"""

import sys
import os
from pathlib import Path

# Добавляем путь к основному проекту для импорта Database
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Проверяем, что путь добавлен
print(f"Added to sys.path: {project_root}")

try:
    from database.db import Database
    print("Database import successful")
except ImportError as e:
    print(f"Database import failed: {e}")
    raise

class DatabaseManager:
    """Менеджер для работы с базой данных"""
    
    def __init__(self):
        # Путь к базе данных из основного проекта
        db_path = project_root / "files" / "databse.db"
        self.db = Database(str(db_path))
        print(f"Database initialized with path: {db_path}")
    
    def get_db(self):
        """Получить экземпляр базы данных"""
        return self.db

# Создаем глобальный экземпляр
db_manager = DatabaseManager()

def get_db():
    """Dependency для FastAPI"""
    return db_manager.get_db()
