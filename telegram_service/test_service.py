"""
Test script for Telegram CRM service
"""
import asyncio
import aiohttp
import json

async def test_telegram_service():
    base_url = "http://localhost:8001"
    
    async with aiohttp.ClientSession() as session:
        # Test health endpoint
        print("Testing health endpoint...")
        async with session.get(f"{base_url}/health") as resp:
            health = await resp.json()
            print(f"Health check: {health}")
        
        # Test getting chats
        print("\nGetting chats...")
        async with session.get(f"{base_url}/api/chats") as resp:
            if resp.status == 200:
                data = await resp.json()
                chats = data.get("chats", [])
                print(f"Found {len(chats)} chats")
                
                # Print first few chats
                for i, chat in enumerate(chats[:3]):
                    print(f"  {i+1}. {chat['name']} ({chat['type']}) - {chat['last_message']}")
                    
                # If we have chats, test getting messages from the first one
                if chats:
                    first_chat = chats[0]
                    print(f"\nGetting messages from '{first_chat['name']}'...")
                    async with session.get(f"{base_url}/api/chats/{first_chat['id']}/messages") as msg_resp:
                        if msg_resp.status == 200:
                            msg_data = await msg_resp.json()
                            messages = msg_data.get("messages", [])
                            total_count = msg_data.get("totalCount", 0)
                            print(f"Found {total_count} messages, showing {len(messages)}:")
                            
                            # Print last few messages
                            for msg in messages[-3:]:
                                sender = "You" if msg['from_me'] else msg.get('sender_name', 'User')
                                print(f"  [{msg['created_at']}] {sender}: {msg['text_content']}")
                        else:
                            print(f"Error getting messages: {msg_resp.status}")
            else:
                print(f"Error getting chats: {resp.status}")

if __name__ == "__main__":
    asyncio.run(test_telegram_service())