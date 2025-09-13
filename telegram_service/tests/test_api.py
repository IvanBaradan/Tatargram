"""
Tests for Telegram API
"""
import pytest
from fastapi.testclient import TestClient
from telegram_api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_chats_without_client():
    # This will test the error handling when client is not initialized
    response = client.get("/api/chats")
    # Since we're not mocking the telegram client, this should return a 503
    assert response.status_code == 503

def test_get_messages_without_client():
    response = client.get("/api/chats/123/messages")
    assert response.status_code == 503

def test_send_message_without_client():
    response = client.post("/api/chats/123/messages", json={"text": "Hello"})
    assert response.status_code == 503

if __name__ == "__main__":
    pytest.main([__file__])