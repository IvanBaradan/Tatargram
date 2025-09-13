"""
API Documentation Generator
"""
import json

def generate_api_docs():
    """Generate API documentation in Markdown format"""
    
    docs = """
# Telegram CRM Service API Documentation

## Overview
The Telegram CRM Service provides a REST API to access Telegram conversations in a format compatible with the existing CRM system.

## Authentication
The API uses the same authentication mechanism as the existing CRM. All endpoints require a valid JWT token in the Authorization header.

```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### Health Check
Check if the service is running.

**GET** `/health`

**Response:**
```json
{
  "status": "healthy"
}
```

### Get Chats
Retrieve all Telegram chats.

**GET** `/api/chats`

**Response:**
```json
{
  "chats": [
    {
      "id": "string",
      "chat_id": "string",
      "user_id": "string",
      "platform": "telegram",
      "name": "string",
      "type": "user|group|channel|supergroup",
      "unread_count": 0,
      "last_message": "string",
      "last_message_date": "2023-01-01T10:00:00Z",
      "photo_url": "string|null",
      "is_verified_read": false,
      "is_no_reply_needed": false,
      "is_pinned": false,
      "account_name": "Telegram"
    }
  ]
}
```

### Get Chat Messages
Retrieve messages from a specific chat.

**GET** `/api/chats/{chat_id}/messages`

**Parameters:**
- `offset` (integer, optional): Pagination offset. Default: 0
- `limit` (integer, optional): Number of messages to return. Default: 50

**Response:**
```json
{
  "messages": [
    {
      "id": "string",
      "message_id": "string",
      "chat_id": "string",
      "from_me": false,
      "created_at": "2023-01-01T10:00:00Z",
      "message_type": "text|media",
      "text_content": "string",
      "media_url": "string|null",
      "is_read": true,
      "is_delivered": true,
      "sender_name": "string",
      "is_edit": false,
      "is_deleted": false
    }
  ],
  "totalCount": 0
}
```

### Send Message
Send a message to a Telegram chat.

**POST** `/api/chats/{chat_id}/messages`

**Request Body:**
```json
{
  "text": "string"
}
```

**Response:**
```json
{
  "status": "sent"
}
```

## WebSocket Endpoint

### Real-time Updates
Connect to receive real-time updates for Telegram messages.

**WebSocket** `/ws/chats/`

**Message Format:**
```json
{
  "event": "new_message",
  "message": {
    // Message object in the same format as GET /api/chats/{chat_id}/messages
  }
}
```

## Error Responses

All endpoints can return the following HTTP status codes:

- `200`: Success
- `400`: Bad Request - Invalid request parameters
- `401`: Unauthorized - Missing or invalid authentication token
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource not found
- `500`: Internal Server Error - Something went wrong on the server
- `503`: Service Unavailable - Telegram client not initialized

**Error Response Format:**
```json
{
  "detail": "Error message"
}
```

## Integration with Existing CRM

To integrate with the existing CRM system:

1. Update the frontend to include Telegram chats in the chat list
2. Modify message display components to handle Telegram messages
3. Add Telegram platform support in the backend models
4. Implement authentication that works with the existing CRM

## Rate Limiting

The API implements rate limiting to prevent abuse:
- 100 requests per minute per IP address
- 1000 requests per hour per authenticated user

Exceeding these limits will result in a 429 (Too Many Requests) response.

## Versioning

The API follows semantic versioning. The current version is v1.0.0.

To specify a version, include it in the Accept header:

```
Accept: application/vnd.telegram-crm.v1+json
```

If no version is specified, the latest version will be used.
"""
    
    # Save to file
    with open("API_DOCS.md", "w", encoding="utf-8") as f:
        f.write(docs)
    
    print("API documentation generated: API_DOCS.md")
    return docs

if __name__ == "__main__":
    generate_api_docs()