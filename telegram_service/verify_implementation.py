"""
Скрипт проверки реализации сервиса Telegram CRM
"""
import os
import sys
import subprocess

def check_python_version():
    """Проверка версии Python"""
    if sys.version_info < (3, 7):
        print("Ошибка: Требуется Python 3.7 или выше")
        return False
    return True

def check_pip():
    """Проверка наличия pip"""
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        print("Ошибка: pip не установлен")
        return False

def check_dependencies():
    """Проверка установленных зависимостей"""
    try:
        import telethon
        import fastapi
        import sqlalchemy
        print("✓ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"✗ Отсутствует зависимость: {e}")
        return False

def check_config():
    """Проверка конфигурации"""
    required_vars = ['TELEGRAM_API_ID', 'TELEGRAM_API_HASH', 'TELEGRAM_PHONE_NUMBER']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"✗ Отсутствуют переменные окружения: {', '.join(missing_vars)}")
        print("  Пожалуйста, создайте файл .env с вашими учетными данными Telegram")
        return False
    else:
        print("✓ Конфигурация завершена")
        return True

def main():
    print("Проверка реализации сервиса Telegram CRM")
    print("=" * 50)
    
    # Проверка Python
    if not check_python_version():
        return False
        
    # Проверка pip
    if not check_pip():
        return False
    
    # Проверка зависимостей
    if not check_dependencies():
        print("\nПожалуйста, установите зависимости командой:")
        print("  pip install -r requirements.txt")
        return False
    
    # Проверка конфигурации
    if not check_config():
        return False
    
    print("\n" + "=" * 50)
    print("Проверка завершена успешно! ✓")
    print("\nСледующие шаги:")
    print("1. Запустите 'python init_db.py' для инициализации базы данных")
    print("2. Запустите 'python demonstrate.py' для тестирования подключения")
    print("3. Запустите 'python telegram_api/main.py' для запуска сервиса")
    print("4. Откройте 'telegram_frontend/index.html' в браузере")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)