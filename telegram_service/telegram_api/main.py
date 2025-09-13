"""
Сервис FastAPI для предоставления бесед Telegram в формате, подобном CRM
"""
import asyncio
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv
from telegram_client.client import TelegramConversationClient
from config import config
from pydantic import BaseModel

# Проверка конфигурации
config_errors = config.validate()
if config_errors:
    raise ValueError(f"Ошибки конфигурации: {', '.join(config_errors)}")

app = FastAPI(title="Сервис Telegram CRM", version="1.0.0")

# Добавление промежуточного ПО CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В производстве укажите точные источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение статических файлов для фронтенда
if os.path.exists("telegram_frontend"):
    app.mount("/frontend", StaticFiles(directory="telegram_frontend", html=True), name="frontend")

# Инициализация клиента Telegram
telegram_client = None

class AuthCode(BaseModel):
    code: str

class Password(BaseModel):
    password: str

@app.on_event("startup")
async def startup_event():
    global telegram_client
    telegram_client = TelegramConversationClient()
    try:
        await telegram_client.connect()
        print("Подключено к Telegram")
    except Exception as e:
        print(f"Не удалось подключиться к Telegram: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    global telegram_client
    if telegram_client:
        await telegram_client.disconnect()
        print("Отключено от Telegram")

@app.get("/")
async def root():
    """Корневая конечная точка, возвращающая приветственное сообщение"""
    return {"message": "Добро пожаловать в Telegram CRM API. Перейдите к /docs для документации API или к /frontend для веб-интерфейса."}

@app.post("/api/auth/code")
async def set_auth_code(auth_code: AuthCode):
    """Установить код аутентификации Telegram"""
    try:
        if not telegram_client:
            raise HTTPException(status_code=503, detail="Клиент Telegram не инициализирован")
        
        telegram_client.set_auth_code(auth_code.code)
        # Попытка повторного подключения с новым кодом
        await telegram_client.connect()
        return {"status": "success", "message": "Код аутентификации установлен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/password")
async def set_password(password: Password):
    """Установить пароль для двухфакторной аутентификации Telegram"""
    try:
        if not telegram_client:
            raise HTTPException(status_code=503, detail="Клиент Telegram не инициализирован")
        
        telegram_client.set_password(password.password)
        return {"status": "success", "message": "Пароль установлен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chats")
async def get_chats():
    """Получить все чаты Telegram в формате CRM"""
    try:
        if not telegram_client:
            raise HTTPException(status_code=503, detail="Клиент Telegram не инициализирован")
        
        chats = await telegram_client.get_chats()
        return {"chats": chats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chats/{chat_id}/messages")
async def get_chat_messages(chat_id: str, offset: int = 0, limit: int = 50):
    """Получить сообщения из определенного чата в формате CRM"""
    try:
        if not telegram_client:
            raise HTTPException(status_code=503, detail="Клиент Telegram не инициализирован")
        
        messages = await telegram_client.get_messages(chat_id, limit)
        
        # Реализация пагинации
        total_count = len(messages)
        if offset == 0:
            # Вернуть последние N сообщений
            start = max(0, total_count - limit)
            end = total_count
        else:
            # Вернуть предыдущие N сообщений
            start = max(0, total_count - offset - limit)
            end = total_count - offset
            
        paginated_messages = messages[start:end]
        
        return {
            "messages": paginated_messages,
            "totalCount": total_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chats/{chat_id}/messages")
async def send_message(chat_id: str, message: dict):
    """Отправить сообщение в чат"""
    try:
        if not telegram_client:
            raise HTTPException(status_code=503, detail="Клиент Telegram не инициализирован")
        
        text = message.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="Текст сообщения обязателен")
        
        success = await telegram_client.send_message(chat_id, text)
        if success:
            return {"status": "sent"}
        else:
            raise HTTPException(status_code=500, detail="Не удалось отправить сообщение")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Конечная точка проверки состояния"""
    return {"status": "healthy"}

# Конечная точка WebSocket для обновлений в реальном времени (аналогично CRM)
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chats/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Обработка входящих сообщений WebSocket
            # Пока просто эхо
            await manager.send_personal_message(f"Вы отправили: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=config.PORT)