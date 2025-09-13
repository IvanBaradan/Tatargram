"""
Модели базы данных для хранения данных Telegram
Это может быть интегрировано с существующей базой данных CRM
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class TelegramChat(Base):
    __tablename__ = 'telegram_chats'
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(String(50), unique=True, nullable=False)
    user_id = Column(String(50), nullable=False)
    platform = Column(String(20), default='telegram')
    name = Column(String(255))
    chat_type = Column(String(20))  # user, group, channel, supergroup
    unread_count = Column(Integer, default=0)
    last_message = Column(Text)
    last_message_date = Column(DateTime)
    photo_url = Column(String(512))
    is_verified_read = Column(Boolean, default=False)
    is_no_reply_needed = Column(Boolean, default=False)
    is_pinned = Column(Boolean, default=False)
    account_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TelegramMessage(Base):
    __tablename__ = 'telegram_messages'
    
    id = Column(Integer, primary_key=True)
    message_id = Column(String(50), unique=True, nullable=False)
    chat_id = Column(String(50), nullable=False)
    from_me = Column(Boolean, default=False)
    created_at = Column(DateTime)
    message_type = Column(String(20))  # text, media, etc.
    text_content = Column(Text)
    media_url = Column(String(512))
    is_read = Column(Boolean, default=True)
    is_delivered = Column(Boolean, default=False)
    sender_name = Column(String(255))
    is_edit = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Настройка базы данных
def get_database_url():
    return os.getenv('DATABASE_URL', 'sqlite:///telegram.db')

def create_tables():
    engine = create_engine(get_database_url())
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = create_engine(get_database_url())
    Session = sessionmaker(bind=engine)
    return Session()

if __name__ == "__main__":
    # Создать таблицы
    engine = create_tables()
    print("Таблицы базы данных успешно созданы!")