# Luna Noir - Promo/Marketing Scripts

## Overview

Simple CLI scripts for posting promotional content to Discord and Reddit with built-in safety throttling.

---

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `requests` - For Discord webhook posting
- `praw>=7.7.0` - Python Reddit API Wrapper

### 2. Configure Environment Variables

Add the following to your `.env` file:

#### Discord Configuration

```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
```

**How to get Discord webhook URL:**
1. Go to your Discord server
2. Right-click on the channel → Edit Channel
3. Go to Integrations → Webhooks
4. Click "New Webhook" or copy existing webhook URL

#### Reddit Configuration

```bash
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=LunaNoirBot/1.0 by your_username
```

**How to get Reddit API credentials:**
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Select "script" as the app type
4. Fill in name, description, redirect URI (use http://localhost:8080)
5. Copy the client ID (under app name) and secret

---

## Usage

### Discord Posting

**Basic usage:**
```bash
python scripts/promo/discord_post.py "Your message here"
```

**Examples:**
```bash
# Simple announcement
python scripts/promo/discord_post.py "Luna Noir is live ✨"

# With Telegram link
python scripts/promo/discord_post.py "Luna Noir is live ✨ DM me on Telegram: t.me/Lunanoircompanionbot"

# With call-to-action
python scripts/promo/discord_post.py "Meet Luna Noir 🌙 Your AI companion is waiting! Chat now: t.me/Lunanoircompanionbot"

# Premium promotion
python scripts/promo/discord_post.py "Luna Noir Premium is here! 💎 Unlock FLIRTY & NSFW modes. Start chatting: t.me/Lunanoircompanionbot"
```

**Default message** (if no argument provided):
```
Luna Noir is live ✨ DM me on Telegram.
```

### Reddit Posting

**Basic usage:**
```bash
python scripts/promo/reddit_post.py <subreddit> "Title" "Body"
```

**Examples:**
```bash
# Test post
python scripts/promo/reddit_post.py test "Luna Noir is live ✨" "DM me on Telegram for a chat."

# AI companions subreddit
python scripts/promo/reddit_post.py AIcompanions "Meet Luna Noir 🌙" "Your AI companion is live! DM me on Telegram: t.me/Lunanoircompanionbot. /upgrade for Premium features (FLIRTY & NSFW modes)."

# Character AI subreddit
python scripts/promo/reddit_post.py CharacterAI "Luna Noir - Your Playful AI Companion" "Hey everyone! 👋 I'm Luna Noir, a warm and playful AI companion available on Telegram. I offer three conversation modes: SAFE (free), FLIRTY, and NSFW (premium). Chat with me: t.me/Lunanoircompanionbot"

# With value content
python scripts/promo/reddit_post.py ChatBots "I built Luna Noir - An AI companion with personality modes" "After months of development, I'm excited to share Luna Noir! She's a Telegram bot with three personality modes (SAFE, FLIRTY, NSFW) and uses GPT-4 for natural conversations. Free tier available. Try her: t.me/Lunanoircompanionbot. Feedback welcome!"
```

**Default values** (if arguments not provided):
- Subreddit: `test`
- Title: `Luna Noir is live ✨`
- Body: `DM me on Telegram for a chat. /upgrade for Premium.`

---

## Safety Guidelines

### ⚠️ IMPORTANT: Respect Platform Rules

#### General Rules
1. **No Spam**: Throttle posts to max 1-2 per day per subreddit/channel
2. **Read Rules**: Always check subreddit/server rules before posting
3. **Add Value**: Don't just advertise - provide value (screenshots, demos, stories)
4. **Be Transparent**: Mention it's your bot/project if relevant
5. **Engage**: Respond to comments and questions

#### Discord-Specific
- Don't post in channels where self-promotion isn't allowed
- Use designated promo/showcase channels
- Don't spam multiple servers at once
- Respect server rate limits

#### Reddit-Specific
- **Check karma requirements**: Many subreddits require minimum karma
- **Read posting rules**: Some subreddits ban self-promotion
- **Use appropriate flair**: Tag posts correctly
- **Avoid cross-posting spam**: Don't post same content to 10+ subreddits
- **Engage with community**: Comment on other posts, don't just promote
- **Wait between posts**: Reddit has built-in rate limiting (10 min between posts for new accounts)

### Content Guidelines

#### ✅ DO:
- Post screenshots of conversations (SFW only)
- Share feature updates and improvements
- Provide clear call-to-action (CTA): "Chat now: t.me/yourbot"
- Mention free tier availability
- Highlight unique features (personality modes, premium features)
- Use emojis sparingly for visual appeal
- Include value proposition (what makes your bot special)

#### ❌ DON'T:
- Post explicit/NSFW content directly
- Spam the same message repeatedly
- Post in unrelated communities
- Use clickbait titles
- Share private conversations without consent
- Violate platform ToS

### Recommended Posting Schedule

**Discord:**
- Max 1 post per channel per day
- Best times: 12pm-2pm, 6pm-9pm (local time)
- Avoid late night/early morning posts

**Reddit:**
- Max 1-2 posts per subreddit per week
- Best times: 8am-10am, 12pm-2pm, 6pm-8pm EST
- Avoid weekends for serious subreddits
- Use weekends for casual/meme subreddits

### Throttling Implementation

Both scripts include built-in safety features:

**Discord:**
- 15-second timeout on requests
- Error handling for rate limits

**Reddit:**
- 2-second delay after posting
- Authentication verification before posting
- Detailed error messages for troubleshooting

### Manual Throttling (Recommended)

Create a posting log to track your activity:

```bash
# Create log file
touch scripts/promo/posting_log.txt

# Log each post
echo "$(date) - Discord - General - Luna Noir announcement" >> scripts/promo/posting_log.txt
echo "$(date) - Reddit - r/AIcompanions - Feature update" >> scripts/promo/posting_log.txt
```

---

## Recommended Subreddits

### AI/Chatbot Communities
- r/ChatBots - General chatbot discussion
- r/AIcompanions - AI companion bots (check rules!)
- r/CharacterAI - Character AI alternatives
- r/OpenAI - OpenAI-powered projects
- r/artificial - AI discussion

### Tech/Development
- r/SideProject - Show off your side projects
- r/IMadeThis - Share what you built
- r/Python - Python projects (if technical post)
- r/Telegram - Telegram bots

### Testing
- r/test - Test posts before going live
- r/FreeKarma4U - Build karma (if needed)

**Note**: Always verify current subreddit rules before posting. Rules change frequently.

---

## Troubleshooting

### Discord Issues

**Error: "DISCORD_WEBHOOK_URL missing"**
- Solution: Add webhook URL to `.env` file

**Error: 404 Not Found**
- Solution: Webhook URL is invalid or deleted. Create new webhook

**Error: 429 Too Many Requests**
- Solution: You're rate-limited. Wait 10+ minutes before posting again

### Reddit Issues

**Error: "praw not installed"**
- Solution: Run `pip install praw>=7.7.0`

**Error: "Missing environment variables"**
- Solution: Add all required Reddit credentials to `.env`

**Error: "Incorrect username or password"**
- Solution: Verify Reddit credentials in `.env`

**Error: "You are doing that too much"**
- Solution: Reddit rate limit. Wait 10+ minutes between posts

**Error: "Subreddit not found"**
- Solution: Check subreddit name spelling (case-sensitive)

**Error: "You aren't allowed to post there"**
- Solution: Check karma requirements or subreddit restrictions

---

## Best Practices

### 1. Create Value-First Posts

Instead of:
> "Check out my bot: t.me/mybot"

Try:
> "I built an AI companion with 3 personality modes (SAFE, FLIRTY, NSFW). Here's a demo conversation [screenshot]. Free tier available. Try it: t.me/mybot"

### 2. Use Engaging Titles

**Good titles:**
- "Meet Luna Noir 🌙 - Your Playful AI Companion"
- "I built an AI chatbot with personality modes - Here's what I learned"
- "Luna Noir Premium: Unlock FLIRTY & NSFW conversation modes"

**Bad titles:**
- "My bot is live"
- "Check this out"
- "Luna Noir"

### 3. Include Screenshots/Demos

- Post SFW conversation screenshots
- Show the inline keyboard UI
- Demonstrate mode switching
- Highlight unique features

### 4. Engage with Responses

- Reply to comments within 1-2 hours
- Answer questions about features
- Thank users for feedback
- Address concerns professionally

### 5. Track Performance

Monitor which posts perform best:
- Upvotes/reactions
- Comments/engagement
- Click-through rate to Telegram
- Conversion to premium

---

## Example Posting Campaign

### Week 1: Launch Announcement

**Discord** (Day 1):
```
Luna Noir is live! 🌙✨

Your playful AI companion is ready to chat on Telegram.
• Free SAFE mode
• Premium FLIRTY & NSFW modes
• Powered by GPT-4

Start chatting: t.me/Lunanoircompanionbot
```

**Reddit r/ChatBots** (Day 3):
```
Title: "Introducing Luna Noir - AI Companion with Personality Modes"

Body: "Hey everyone! I just launched Luna Noir, a Telegram AI companion bot with three conversation modes:

• SAFE (Free) - Warm, playful, helpful assistant
• FLIRTY (Premium) - Light flirtation, PG-13
• NSFW (Premium) - Adult conversations (within platform rules)

Built with GPT-4, Stripe payments, and per-user mode persistence. Free tier available for everyone.

Try her: t.me/Lunanoircompanionbot

Would love your feedback!"
```

### Week 2: Feature Highlight

**Discord** (Day 8):
```
Luna Noir Premium is here! 💎

Unlock exclusive features:
✓ FLIRTY & NSFW conversation modes
✓ Longer responses
✓ Extended conversation memory

Free tier still available!
Chat now: t.me/Lunanoircompanionbot
```

### Week 3: User Testimonial

**Reddit r/AIcompanions** (Day 15):
```
Title: "Luna Noir Update - Premium Features & User Feedback"

Body: "Thanks for the amazing response! Luna Noir has been live for 2 weeks and here's what users are saying:

[Include positive feedback/testimonials]

Recent updates:
• Improved response quality
• Faster reply times
• Better mode switching UI

Try the free tier: t.me/Lunanoircompanionbot
Premium: /upgrade command"
```

---

## Legal & Compliance

### Terms of Service Compliance

**Discord:**
- Follow Discord Community Guidelines
- No sexually explicit content in public channels
- Respect server rules and moderators

**Reddit:**
- Follow Reddit Content Policy
- No spam or vote manipulation
- Respect subreddit rules

**Telegram:**
- Follow Telegram Terms of Service
- No illegal content
- Respect user privacy

### Content Warnings

When promoting NSFW features:
- ✅ "Premium NSFW mode available (18+)"
- ✅ "Adult conversations within platform rules"
- ❌ Don't post explicit examples
- ❌ Don't share NSFW screenshots

---

## Support

For issues with the promo scripts:
1. Check environment variables in `.env`
2. Verify API credentials are correct
3. Review error messages for specific issues
4. Check platform status pages (Discord, Reddit)

For bot issues:
- See main README.md
- Check bot logs
- Test with `/start` command

---

## Summary

✅ **Discord posting**: Simple webhook-based posting  
✅ **Reddit posting**: PRAW-based with authentication  
✅ **Safety throttling**: Built-in delays and error handling  
✅ **Environment variables**: Secure credential storage  
✅ **Best practices**: Detailed guidelines for responsible promotion  

**Remember**: Quality over quantity. One valuable post is better than 10 spam posts.

Happy promoting! 🚀

