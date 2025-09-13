"""
Complete workflow demonstration
"""
import asyncio
import os
import sys
from telegram_client.client import TelegramConversationClient
from telegram_client.models import create_tables, get_session, TelegramChat, TelegramMessage

async def demonstrate_workflow():
    """Demonstrate the complete workflow of the Telegram CRM service"""
    print("Telegram CRM Service - Workflow Demonstration")
    print("=" * 50)
    
    # 1. Initialize database
    print("1. Initializing database...")
    engine = create_tables()
    print(f"   Database created at: {engine.url}")
    
    # 2. Connect to Telegram
    print("\n2. Connecting to Telegram...")
    client = TelegramConversationClient()
    
    try:
        await client.connect()
        print("   ✓ Connected to Telegram successfully")
        
        # 3. Fetch chats
        print("\n3. Fetching Telegram chats...")
        chats = await client.get_chats()
        print(f"   Found {len(chats)} chats")
        
        if chats:
            # Display first few chats
            print("   Sample chats:")
            for i, chat in enumerate(chats[:3]):
                print(f"     {i+1}. {chat['name']} ({chat['type']})")
            
            # 4. Fetch messages from first chat
            first_chat = chats[0]
            print(f"\n4. Fetching messages from '{first_chat['name']}'...")
            messages = await client.get_messages(first_chat['id'], limit=10)
            print(f"   Retrieved {len(messages)} messages")
            
            if messages:
                print("   Sample messages:")
                for msg in messages[-3:]:  # Show last 3 messages
                    sender = "You" if msg['from_me'] else msg.get('sender_name', 'User')
                    print(f"     [{msg['created_at']}] {sender}: {msg['text_content'][:50]}...")
            
            # 5. Save to database
            print("\n5. Saving data to database...")
            session = get_session()
            
            try:
                # Save chat
                db_chat = TelegramChat(
                    chat_id=first_chat['chat_id'],
                    user_id=first_chat['user_id'],
                    platform=first_chat['platform'],
                    name=first_chat['name'],
                    chat_type=first_chat['type'],
                    last_message=first_chat['last_message'],
                    last_message_date=first_chat['last_message_date'],
                    photo_url=first_chat['photo_url'],
                    is_verified_read=first_chat['is_verified_read'],
                    is_no_reply_needed=first_chat['is_no_reply_needed'],
                    is_pinned=first_chat['is_pinned'],
                    account_name=first_chat['account_name']
                )
                session.add(db_chat)
                session.commit()
                print("   ✓ Chat saved to database")
                
                # Save messages
                for msg in messages:
                    db_msg = TelegramMessage(
                        message_id=msg['message_id'],
                        chat_id=msg['chat_id'],
                        from_me=msg['from_me'],
                        created_at=msg['created_at'],
                        message_type=msg['message_type'],
                        text_content=msg['text_content'],
                        media_url=msg['media_url'],
                        is_read=msg['is_read'],
                        is_delivered=msg['is_delivered'],
                        sender_name=msg['sender_name'],
                        is_edit=msg['is_edit'],
                        is_deleted=msg['is_deleted']
                    )
                    session.add(db_msg)
                
                session.commit()
                print(f"   ✓ {len(messages)} messages saved to database")
                
            except Exception as e:
                print(f"   ✗ Error saving to database: {e}")
                session.rollback()
            finally:
                session.close()
                
        else:
            print("   No chats found")
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        
    finally:
        # 6. Disconnect
        print("\n6. Disconnecting from Telegram...")
        await client.disconnect()
        print("   ✓ Disconnected from Telegram")
        
    print("\n" + "=" * 50)
    print("Workflow demonstration completed!")

if __name__ == "__main__":
    # Check if environment variables are set
    required_vars = ['TELEGRAM_API_ID', 'TELEGRAM_API_HASH', 'TELEGRAM_PHONE_NUMBER']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        sys.exit(1)
    
    # Run the demonstration
    asyncio.run(demonstrate_workflow())