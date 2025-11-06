# Promo Scripts - Quick Examples

## Discord Examples

### Basic Announcement
```bash
python scripts/promo/discord_post.py "Luna Noir is live ✨"
```

### With Telegram Link
```bash
python scripts/promo/discord_post.py "Luna Noir is live ✨ DM me on Telegram: t.me/Lunanoircompanionbot"
```

### Premium Promotion
```bash
python scripts/promo/discord_post.py "Luna Noir Premium is here! 💎 Unlock FLIRTY & NSFW modes. Start chatting: t.me/Lunanoircompanionbot"
```

### Feature Update
```bash
python scripts/promo/discord_post.py "🎉 New Update! Luna Noir now has improved conversation memory and faster responses. Try it: t.me/Lunanoircompanionbot"
```

---

## Reddit Examples

### Test Post (r/test)
```bash
python scripts/promo/reddit_post.py test "Luna Noir Test Post" "Testing the bot posting functionality."
```

### AI Companions Subreddit
```bash
python scripts/promo/reddit_post.py AIcompanions "Meet Luna Noir 🌙 - Your Playful AI Companion" "Your AI companion is live on Telegram! 

Features:
• SAFE mode (Free) - Warm, playful, helpful
• FLIRTY mode (Premium) - Light flirtation, PG-13
• NSFW mode (Premium) - Adult conversations

Powered by GPT-4 with per-user conversation memory.

Try the free tier: t.me/Lunanoircompanionbot
Upgrade: /upgrade command"
```

### ChatBots Subreddit
```bash
python scripts/promo/reddit_post.py ChatBots "I built Luna Noir - An AI companion with personality modes" "After months of development, I'm excited to share Luna Noir! 

She's a Telegram bot with three personality modes:
• SAFE (free) - Friendly assistant
• FLIRTY (premium) - Playful conversations  
• NSFW (premium) - Adult content

Tech stack:
• Python + python-telegram-bot
• GPT-4 via OpenAI API
• Stripe for payments
• Flask webhook server
• Deployed on Railway

Free tier available. Try her: t.me/Lunanoircompanionbot

Feedback welcome!"
```

### Side Project Subreddit
```bash
python scripts/promo/reddit_post.py SideProject "Luna Noir - AI Companion Bot with Premium Tiers" "Built a Telegram AI companion bot as a side project!

Key features:
✓ Three conversation modes (SAFE/FLIRTY/NSFW)
✓ Freemium model with Stripe integration
✓ Per-user mode persistence
✓ Inline keyboard controls
✓ GPT-4 powered responses

Tech: Python, Flask, Telegram Bot API, Stripe, Railway

Live demo: t.me/Lunanoircompanionbot

Happy to answer questions about the tech stack or monetization!"
```

### Telegram Subreddit
```bash
python scripts/promo/reddit_post.py Telegram "Luna Noir - AI Companion Bot for Telegram" "Just launched Luna Noir, an AI companion bot for Telegram!

Features:
• Inline keyboard for mode switching
• Per-user conversation memory
• Premium subscription via Stripe
• Webhook-based (no polling)
• Deployed on Railway

Try it: t.me/Lunanoircompanionbot

Open to feedback from the Telegram bot community!"
```

---

## Safety Reminders

### Before Posting:

1. **Check subreddit rules**
   ```bash
   # Visit subreddit and read rules
   open "https://reddit.com/r/SUBREDDIT_NAME/about/rules"
   ```

2. **Verify you're not rate-limited**
   - Wait 10+ minutes between Reddit posts
   - Wait 1+ hour between Discord posts to same channel

3. **Log your posts**
   ```bash
   echo "$(date) - Reddit - r/AIcompanions - Launch announcement" >> scripts/promo/posting_log.txt
   ```

4. **Review content**
   - No explicit content
   - Clear call-to-action
   - Value proposition included
   - Proper formatting

### Recommended Schedule:

**Week 1:**
- Day 1: Discord announcement
- Day 3: Reddit r/ChatBots
- Day 5: Reddit r/SideProject

**Week 2:**
- Day 8: Discord feature update
- Day 10: Reddit r/AIcompanions
- Day 12: Reddit r/Telegram

**Week 3:**
- Day 15: Discord premium promo
- Day 17: Reddit r/IMadeThis
- Day 19: Reddit r/Python (if technical post)

---

## Troubleshooting

### Discord: "DISCORD_WEBHOOK_URL missing"
```bash
# Add to .env:
echo 'DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_ID/YOUR_TOKEN' >> .env
```

### Reddit: "praw not installed"
```bash
pip install praw>=7.7.0
```

### Reddit: "Missing environment variables"
```bash
# Add to .env:
cat >> .env << 'EOF'
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
REDDIT_USER_AGENT=LunaNoirBot/1.0 by your_username
EOF
```

### Test Before Going Live:
```bash
# Test Discord (if webhook configured)
python scripts/promo/discord_post.py "Test message - please ignore"

# Test Reddit on r/test
python scripts/promo/reddit_post.py test "Test Post" "Testing bot functionality"
```

---

## Quick Reference

| Platform | Max Frequency | Best Times (EST) | Character Limit |
|----------|---------------|------------------|-----------------|
| Discord  | 1/day/channel | 12pm-2pm, 6pm-9pm | 2000 chars |
| Reddit   | 1-2/week/sub  | 8am-10am, 12pm-2pm | Title: 300, Body: 40000 |

**Remember**: Quality > Quantity. One great post beats 10 mediocre ones.

