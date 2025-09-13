"""
Конфигурация для сервиса Telegram
"""
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

class Config:
    # Учетные данные API Telegram
    TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
    TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
    TELEGRAM_PHONE_NUMBER = os.getenv('TELEGRAM_PHONE_NUMBER')
    
    # Конфигурация базы данных
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///telegram.db')
    
    # Конфигурация веб-сервера
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8001))
    
    # Файл сессии
    SESSION_FILE = os.getenv('SESSION_FILE', 'telegram_session')
    
    # Безопасность
    SECRET_KEY = os.getenv('SECRET_KEY', 'telegram-crm-secret-key')
    
    @classmethod
    def validate(cls):
        """Проверка обязательной конфигурации"""
        errors = []
        
        if not cls.TELEGRAM_API_ID:
            errors.append("TELEGRAM_API_ID обязателен")
            
        if not cls.TELEGRAM_API_HASH:
            errors.append("TELEGRAM_API_HASH обязателен")
            
        if not cls.TELEGRAM_PHONE_NUMBER:
            errors.append("TELEGRAM_PHONE_NUMBER обязателен")
            
        return errors

# Создание экземпляра конфигурации
config = Config()