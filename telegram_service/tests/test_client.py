"""
Tests for Telegram client
"""
import pytest
import asyncio
from unittest.mock import Mock, patch
from telegram_client.client import TelegramConversationClient

@pytest.fixture
def telegram_client():
    with patch('telegram_client.client.TelegramClient') as mock_client:
        client = TelegramConversationClient()
        client.client = mock_client
        yield client

@pytest.mark.asyncio
async def test_get_chats(telegram_client):
    # Mock the get_dialogs method
    mock_dialog = Mock()
    mock_entity = Mock()
    mock_entity.id = 123456789
    mock_entity.first_name = "John"
    mock_entity.last_name = "Doe"
    mock_dialog.entity = mock_entity
    mock_dialog.unread_count = 0
    mock_dialog.message = "Hello"
    mock_dialog.date.isoformat.return_value = "2023-01-01T10:00:00Z"
    
    telegram_client.client.get_dialogs.return_value = [mock_dialog]
    
    # Test the method
    chats = await telegram_client.get_chats()
    
    # Assertions
    assert len(chats) == 1
    assert chats[0]['id'] == '123456789'
    assert chats[0]['name'] == 'John Doe'
    assert chats[0]['platform'] == 'telegram'

@pytest.mark.asyncio
async def test_get_messages(telegram_client):
    # Mock the get_entity and GetHistoryRequest
    mock_entity = Mock()
    telegram_client.client.get_entity.return_value = mock_entity
    
    # Mock message
    mock_message = Mock()
    mock_message.id = 987654321
    mock_message.message = "Test message"
    mock_message.date.isoformat.return_value = "2023-01-01T10:00:00Z"
    mock_message.out = False
    mock_message.media = None
    mock_message.sender_id = None
    
    # Mock GetHistoryRequest response
    mock_messages = Mock()
    mock_messages.messages = [mock_message]
    telegram_client.client.return_value = mock_messages
    
    with patch('telegram_client.client.GetHistoryRequest') as mock_request:
        mock_request.return_value = mock_request
        telegram_client.client.return_value = mock_messages
        
        # Test the method
        messages = await telegram_client.get_messages('123456789')
        
        # Assertions
        assert len(messages) == 1
        assert messages[0]['id'] == '987654321'
        assert messages[0]['text_content'] == 'Test message'
        assert messages[0]['from_me'] == False

if __name__ == "__main__":
    pytest.main([__file__])