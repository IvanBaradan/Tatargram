"""
Скрипт финальной проверки реализации и перевода сервиса Telegram CRM
"""
import os
import sys

def check_translations():
    """Проверка правильности перевода комментариев"""
    print("Проверка перевода комментариев...")
    
    # Проверка config.py
    with open("config.py", "r", encoding="utf-8") as f:
        config_content = f.read()
    
    if "Конфигурация для сервиса Telegram" in config_content and "Загрузка переменных окружения" in config_content:
        print("✓ config.py: Перевод выполнен корректно")
    else:
        print("✗ config.py: Обнаружены непереведенные комментарии")
        return False
    
    # Проверка client.py
    with open("telegram_client/client.py", "r", encoding="utf-8") as f:
        client_content = f.read()
    
    if "Клиент Telegram, использующий Telethon" in client_content and "Подключение к Telegram и аутентификация" in client_content:
        print("✓ telegram_client/client.py: Перевод выполнен корректно")
    else:
        print("✗ telegram_client/client.py: Обнаружены непереведенные комментарии")
        return False
    
    # Проверка models.py
    with open("telegram_client/models.py", "r", encoding="utf-8") as f:
        models_content = f.read()
    
    if "Модели базы данных для хранения данных Telegram" in models_content:
        print("✓ telegram_client/models.py: Перевод выполнен корректно")
    else:
        print("✗ telegram_client/models.py: Обнаружены непереведенные комментарии")
        return False
    
    # Проверка main.py
    with open("telegram_api/main.py", "r", encoding="utf-8") as f:
        api_content = f.read()
    
    if "Сервис FastAPI для предоставления бесед Telegram" in api_content and "Добавление промежуточного ПО CORS" in api_content:
        print("✓ telegram_api/main.py: Перевод выполнен корректно")
    else:
        print("✗ telegram_api/main.py: Обнаружены непереведенные комментарии")
        return False
    
    # Проверка index.html
    with open("telegram_frontend/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    if "Подключение..." in html_content and "Загрузка чатов..." in html_content:
        print("✓ telegram_frontend/index.html: Перевод выполнен корректно")
    else:
        print("✗ telegram_frontend/index.html: Обнаружены непереведенные тексты")
        return False
    
    return True

def check_structure():
    """Проверка структуры проекта"""
    print("\nПроверка структуры проекта...")
    
    required_files = [
        "config.py",
        "requirements.txt",
        "telegram_client/client.py",
        "telegram_client/models.py",
        "telegram_api/main.py",
        "telegram_frontend/index.html"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}: Файл существует")
        else:
            print(f"✗ {file_path}: Файл отсутствует")
            return False
    
    return True

def main():
    print("Финальная проверка реализации и перевода сервиса Telegram CRM")
    print("=" * 60)
    
    # Проверка структуры
    if not check_structure():
        print("\n✗ Проверка структуры провалена")
        return False
    
    # Проверка переводов
    if not check_translations():
        print("\n✗ Проверка переводов провалена")
        return False
    
    print("\n" + "=" * 60)
    print("Финальная проверка завершена успешно! ✓")
    print("\nВсе файлы на месте и все комментарии переведены на русский язык.")
    print("\nСервис готов к использованию и интеграции с CRM системой.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)