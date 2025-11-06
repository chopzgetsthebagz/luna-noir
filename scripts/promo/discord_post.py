#!/usr/bin/env python3
"""
Discord Promo Posting Script
Posts promotional messages to Discord via webhook.

Usage:
    python scripts/promo/discord_post.py "Your message here"
    
Example:
    python scripts/promo/discord_post.py "Luna Noir is live ✨ DM me on Telegram: t.me/Lunanoircompanionbot"

Environment Variables Required:
    DISCORD_WEBHOOK_URL - Discord webhook URL from channel settings
"""

import os
import json
import requests
import sys
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

# Get webhook URL
HOOK = os.getenv("DISCORD_WEBHOOK_URL")
assert HOOK, "DISCORD_WEBHOOK_URL missing in .env file"

# Get message content
content = sys.argv[1] if len(sys.argv) > 1 else "Luna Noir is live ✨ DM me on Telegram."

# Post to Discord
try:
    r = requests.post(HOOK, json={"content": content}, timeout=15)
    print(f"Discord: {r.status_code}")
    if r.status_code == 204:
        print("✅ Message posted successfully!")
    else:
        print(f"Response: {r.text[:200]}")
except Exception as e:
    print(f"❌ Error posting to Discord: {e}")
    sys.exit(1)

