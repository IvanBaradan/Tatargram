"""
Клиент Telegram, использующий Telethon для получения пользовательских бесед
"""
import asyncio
import logging
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel, User, Chat, Channel
import os
from dotenv import load_dotenv
from datetime import datetime

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramConversationClient:
    def __init__(self):
        # Получение учетных данных из переменных окружения
        self.api_id = int(os.getenv('TELEGRAM_API_ID'))
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.phone_number = os.getenv('TELEGRAM_PHONE_NUMBER')
        
        # Используем абсолютный путь для файла сессии в домашней директории пользователя
        home_dir = os.path.expanduser("~")
        session_path = os.path.join(home_dir, 'telegram_session')
        logger.info(f"Using session path: {session_path}")
        
        # Инициализация клиента
        self.client = TelegramClient(session_path, self.api_id, self.api_hash)
        self.phone_code = None
        self.password = None
        
    async def connect(self):
        """Подключение к Telegram и аутентификация"""
        await self.client.connect()
        
        # Проверка авторизации
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            if self.phone_code:
                try:
                    await self.client.sign_in(self.phone_number, self.phone_code)
                except SessionPasswordNeededError:
                    if self.password:
                        await self.client.sign_in(password=self.password)
            else:
                logger.warning("Требуется код подтверждения. Используйте метод set_auth_code для установки кода.")
                
    def set_auth_code(self, code):
        """Установить код аутентификации"""
        self.phone_code = code
        
    def set_password(self, password):
        """Установить пароль для двухфакторной аутентификации"""
        self.password = password
                
    async def get_chats(self):
        """Получить все чаты в формате, подобном CRM"""
        dialogs = await self.client.get_dialogs()
        chats = []
        
        for dialog in dialogs:
            chat = dialog.entity
            
            # Определение типа чата и имени
            if isinstance(chat, User):
                chat_type = "user"
                title = f"{chat.first_name or ''} {chat.last_name or ''}".strip()
                if not title:
                    title = chat.username or f"Пользователь {chat.id}"
            elif isinstance(chat, Chat):
                chat_type = "group"
                title = chat.title
            elif isinstance(chat, Channel):
                chat_type = "channel" if chat.broadcast else "supergroup"
                title = chat.title
            else:
                chat_type = "unknown"
                title = str(chat)
            
            # Получить URL фото, если доступно
            photo_url = None
            if hasattr(chat, 'photo') and chat.photo:
                # В реальной реализации вы бы скачали и обслужили фото
                photo_url = f"/api/chats/{chat.id}/photo"  # Заполнитель
            
            chat_info = {
                'id': str(chat.id),
                'chat_id': str(chat.id),
                'user_id': str(chat.id),  # Для согласованности с CRM
                'platform': 'telegram',
                'name': title,
                'type': chat_type,
                'unread_count': dialog.unread_count,
                'last_message': str(dialog.message)[:100] if dialog.message else '',
                'last_message_date': dialog.date.isoformat() if dialog.date else None,
                'photo_url': photo_url,
                'is_verified_read': False,
                'is_no_reply_needed': False,
                'is_pinned': False,
                'account_name': 'Telegram'
            }
            chats.append(chat_info)
            
        return chats
    
    async def get_messages(self, chat_id, limit=50):
        """Получить сообщения из определенного чата в формате, подобном CRM"""
        try:
            # Получить сущность для чата
            entity = await self.client.get_entity(int(chat_id))
            
            # Получить историю сообщений
            messages = await self.client(GetHistoryRequest(
                peer=entity,
                limit=limit,
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0
            ))
            
            message_list = []
            for msg in messages.messages:
                if hasattr(msg, 'message') and msg.message:
                    # Определить тип сообщения
                    message_type = "text"
                    if msg.media:
                        message_type = "media"
                    
                    # Определить отправителя
                    from_me = msg.out
                    sender_name = "Вы" if from_me else ""
                    
                    # Попытаться получить информацию об отправителе
                    if not from_me and msg.sender_id:
                        try:
                            sender = await self.client.get_entity(msg.sender_id)
                            if isinstance(sender, User):
                                sender_name = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
                                if not sender_name:
                                    sender_name = sender.username or f"Пользователь {sender.id}"
                        except:
                            sender_name = f"Пользователь {msg.sender_id}"
                    
                    message_info = {
                        'id': str(msg.id),
                        'message_id': str(msg.id),
                        'chat_id': str(chat_id),
                        'from_me': from_me,
                        'created_at': msg.date.isoformat() if msg.date else None,
                        'message_type': message_type,
                        'text_content': msg.message,
                        'media_url': None,  # Нужно реализовать обработку медиа
                        'is_read': True,  # Сообщения Telegram обычно прочитаны
                        'is_delivered': True,
                        'sender_name': sender_name,
                        'is_edit': False,
                        'is_deleted': False
                    }
                    message_list.append(message_info)
                    
            # Сортировать сообщения по дате (сначала старые)
            message_list.sort(key=lambda x: x['created_at'] or '')
            return message_list
        except Exception as e:
            logger.error(f"Ошибка получения сообщений для чата {chat_id}: {e}")
            return []
    
    async def send_message(self, chat_id, text):
        """Отправить сообщение в чат"""
        try:
            entity = await self.client.get_entity(int(chat_id))
            await self.client.send_message(entity, text)
            return True
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения в чат {chat_id}: {e}")
            return False
    
    async def disconnect(self):
        """Отключение от Telegram"""
        await self.client.disconnect()

# Пример использования
async def main():
    client = TelegramConversationClient()
    try:
        await client.connect()
        print("Подключено к Telegram!")
        
        # Получить чаты
        chats = await client.get_chats()
        print(f"Найдено {len(chats)} чатов")
        
        # Получить сообщения из первого чата
        if chats:
            first_chat = chats[0]
            print(f"Получение сообщений от {first_chat['name']}")
            messages = await client.get_messages(first_chat['id'])
            print(f"Получено {len(messages)} сообщений")
            
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())