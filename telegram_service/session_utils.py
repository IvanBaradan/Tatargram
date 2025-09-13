"""
Session management utilities
"""
import os
import sys
from telegram_client.client import TelegramConversationClient

async def check_session():
    """Check if Telegram session is valid"""
    print("Checking Telegram session...")
    
    client = TelegramConversationClient()
    
    try:
        await client.connect()
        print("✓ Session is valid and connected")
        
        # Try to fetch basic info
        me = await client.client.get_me()
        print(f"✓ Authenticated as: {me.first_name} {me.last_name or ''} (@{me.username or 'N/A'})")
        
        await client.disconnect()
        return True
        
    except Exception as e:
        print(f"✗ Session error: {e}")
        return False

async def remove_session():
    """Remove Telegram session file"""
    session_file = "telegram_session.session"
    
    if os.path.exists(session_file):
        try:
            os.remove(session_file)
            print(f"✓ Removed session file: {session_file}")
            return True
        except Exception as e:
            print(f"✗ Error removing session file: {e}")
            return False
    else:
        print(f"Session file {session_file} does not exist")
        return True

async def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python session_utils.py check    - Check if session is valid")
        print("  python session_utils.py remove   - Remove session file")
        return
    
    command = sys.argv[1].lower()
    
    if command == "check":
        await check_session()
    elif command == "remove":
        await remove_session()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: check, remove")

if __name__ == "__main__":
    asyncio.run(main())