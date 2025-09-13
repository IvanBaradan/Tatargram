# Telegram CRM Service

A service that pulls Telegram user conversations and displays them in a CRM-like interface, using the existing CRM folder as a visual reference.

## Features

- Fetch Telegram conversations using Telethon (MTProto)
- Display chats and messages in a web interface similar to the CRM
- Send messages to Telegram contacts
- REST API for integration with other services

## Prerequisites

1. Python 3.9+
2. Telegram API credentials (get from https://my.telegram.org/)
3. Docker (optional, for containerized deployment)

## Setup

1. Clone the repository
2. Create a `.env` file based on `.env.example`:
   ```
   TELEGRAM_API_ID=your_api_id_here
   TELEGRAM_API_HASH=your_api_hash_here
   TELEGRAM_PHONE_NUMBER=your_phone_number_here
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running with Python

1. Start the API server:
   ```
   python telegram_api/main.py
   ```

2. Open `telegram_frontend/index.html` in a web browser

### Running with Docker

1. Build and start the service:
   ```
   docker-compose up --build
   ```

2. Open `http://localhost:8001` in a web browser

## API Endpoints

- `GET /api/chats` - Get all Telegram chats
- `GET /api/chats/{chat_id}/messages` - Get messages from a specific chat
- `POST /api/chats/{chat_id}/messages` - Send a message to a chat
- `GET /health` - Health check

## Directory Structure

```
telegram_service/
├── telegram_client/     # Telegram client implementation
├── telegram_api/        # FastAPI service
├── telegram_frontend/   # Web frontend
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── .env.example        # Environment variables template
└── README.md           # This file
```

## Authentication

The first time you run the service, you'll need to authenticate with Telegram:

1. Run the service
2. Enter the phone number when prompted
3. Enter the code sent to your Telegram app
4. If you have 2FA enabled, enter your password

The session will be saved in `telegram_session.session` for future use.

## Integration with Existing CRM

To integrate with the existing CRM system:

1. Modify the frontend to match the CRM's styling and layout
2. Update the API endpoints to match the CRM's data structure
3. Add authentication that matches the CRM's user system
4. Implement WebSocket connections similar to the CRM's chat system

## License

MIT