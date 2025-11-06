#!/usr/bin/env python3
"""
Reddit Promo Posting Script
Posts promotional content to Reddit using PRAW.

Usage:
    python scripts/promo/reddit_post.py <subreddit> "Title" "Body"
    
Examples:
    python scripts/promo/reddit_post.py test "Luna Noir is live ✨" "DM me on Telegram for a chat."
    python scripts/promo/reddit_post.py AIcompanions "Meet Luna Noir 🌙" "Your AI companion is live! DM me on Telegram: t.me/Lunanoircompanionbot. /upgrade for Premium features."

Environment Variables Required:
    REDDIT_CLIENT_ID - Reddit app client ID
    REDDIT_CLIENT_SECRET - Reddit app client secret
    REDDIT_USERNAME - Your Reddit username
    REDDIT_PASSWORD - Your Reddit password
    REDDIT_USER_AGENT - User agent string (default: LunaNoirBot/1.0)

Safety Notes:
    - Always check subreddit rules before posting
    - Avoid spam - throttle posts (max 1-2 per day per subreddit)
    - Use value posts (screenshots, clips) + CTA
    - Don't post explicit content; link to Telegram instead
"""

import os
import sys
import time
from pathlib import Path

try:
    import praw
except ImportError:
    print("❌ Error: praw not installed. Run: pip install praw>=7.7.0")
    sys.exit(1)

# Load environment variables
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

# Get arguments
SUB = sys.argv[1] if len(sys.argv) > 1 else "test"
TITLE = sys.argv[2] if len(sys.argv) > 2 else "Luna Noir is live ✨"
BODY = sys.argv[3] if len(sys.argv) > 3 else "DM me on Telegram for a chat. /upgrade for Premium."

# Validate environment variables
required_vars = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME", "REDDIT_PASSWORD"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    print(f"❌ Error: Missing environment variables: {', '.join(missing_vars)}")
    print("Please set them in .env file")
    sys.exit(1)

# Initialize Reddit client
try:
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
        user_agent=os.getenv("REDDIT_USER_AGENT", "LunaNoirBot/1.0")
    )
    
    # Test authentication
    print(f"✓ Authenticated as: {reddit.user.me()}")
    
except Exception as e:
    print(f"❌ Error authenticating with Reddit: {e}")
    sys.exit(1)

# Post to subreddit
try:
    print(f"\nPosting to r/{SUB}...")
    print(f"Title: {TITLE}")
    print(f"Body: {BODY[:100]}{'...' if len(BODY) > 100 else ''}")
    
    post = reddit.subreddit(SUB).submit(title=TITLE, selftext=BODY)
    
    print(f"\n✅ Post created successfully!")
    print(f"URL: https://reddit.com{post.permalink}")
    
    # Safety throttle
    time.sleep(2)
    
except Exception as e:
    print(f"\n❌ Error posting to Reddit: {e}")
    print("\nTroubleshooting:")
    print("  - Check if subreddit exists and allows text posts")
    print("  - Verify you have enough karma to post")
    print("  - Check subreddit rules for posting requirements")
    print("  - Ensure you're not rate-limited (wait 10+ minutes between posts)")
    sys.exit(1)

