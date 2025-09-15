"""
Конфигурация для Web App
"""

# URL вашего Web App (HTTP для тестирования)
WEBAPP_URL = "http://testdlyavsego.ru"

# Альтернативные URL для разработки
WEBAPP_URL_DEV = "http://localhost:3000"
WEBAPP_URL_STAGING = "https://staging.testdlyavsego.ru"

# Функция для получения URL в зависимости от окружения
def get_webapp_url():
    import os
    env = os.getenv('ENVIRONMENT', 'production')
    
    if env == 'development':
        return WEBAPP_URL_DEV
    elif env == 'staging':
        return WEBAPP_URL_STAGING
    else:
        return WEBAPP_URL
