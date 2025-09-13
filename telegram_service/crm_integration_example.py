"""
Example script showing how to integrate Telegram service with existing CRM
This would be added to the CRM codebase
"""
import requests
import json
from typing import List, Dict

class TelegramCRMIntegration:
    def __init__(self, telegram_service_url: str = "http://localhost:8001"):
        self.service_url = telegram_service_url
        
    def get_telegram_chats(self) -> List[Dict]:
        """
        Fetch Telegram chats and format them to match CRM structure
        """
        try:
            response = requests.get(f"{self.service_url}/api/chats")
            if response.status_code == 200:
                data = response.json()
                return data.get("chats", [])
            else:
                print(f"Error fetching Telegram chats: {response.status_code}")
                return []
        except Exception as e:
            print(f"Exception fetching Telegram chats: {e}")
            return []
            
    def get_telegram_messages(self, chat_id: str, offset: int = 0, limit: int = 50) -> Dict:
        """
        Fetch Telegram messages for a specific chat
        """
        try:
            params = {"offset": offset, "limit": limit}
            response = requests.get(f"{self.service_url}/api/chats/{chat_id}/messages", params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching Telegram messages: {response.status_code}")
                return {"messages": [], "totalCount": 0}
        except Exception as e:
            print(f"Exception fetching Telegram messages: {e}")
            return {"messages": [], "totalCount": 0}
            
    def send_telegram_message(self, chat_id: str, text: str) -> bool:
        """
        Send a message to a Telegram chat
        """
        try:
            payload = {"text": text}
            response = requests.post(f"{self.service_url}/api/chats/{chat_id}/messages", json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Exception sending Telegram message: {e}")
            return False
            
    def merge_with_crm_chats(self, crm_chats: List[Dict]) -> List[Dict]:
        """
        Merge Telegram chats with existing CRM chats
        """
        telegram_chats = self.get_telegram_chats()
        
        # Add platform identifier to distinguish Telegram chats
        for chat in telegram_chats:
            chat["platform"] = "telegram"
            
        # Combine CRM and Telegram chats
        all_chats = crm_chats + telegram_chats
        
        # Sort by last message date (newest first)
        all_chats.sort(key=lambda x: x.get("last_message_date", ""), reverse=True)
        
        return all_chats

# Example usage (this would be integrated into the CRM frontend)
def example_usage():
    # Initialize the integration
    telegram_crm = TelegramCRMIntegration("http://localhost:8001")
    
    # Example: Get all chats (including Telegram)
    # Normally this would come from the existing CRM
    crm_chats = [
        {
            "id": "whatsapp_123",
            "chat_id": "123",
            "user_id": "123",
            "platform": "whatsapp",
            "name": "John Doe (WhatsApp)",
            "last_message": "Hello from WhatsApp",
            "last_message_date": "2023-01-01T10:00:00Z"
        }
    ]
    
    # Merge with Telegram chats
    all_chats = telegram_crm.merge_with_crm_chats(crm_chats)
    
    print(f"Total chats: {len(all_chats)}")
    for chat in all_chats:
        print(f"- {chat['name']} ({chat['platform']})")

if __name__ == "__main__":
    example_usage()