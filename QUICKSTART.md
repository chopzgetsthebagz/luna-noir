# Luna Noir Bot - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Get Your Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the prompts to create your bot
4. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your bot token
# Change this line:
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
# To:
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### Step 3: Install Dependencies

```bash
# Install all required packages
make install

# Or manually:
pip install -r requirements.txt
```

### Step 4: Run the Bot (Local Development)

#### Option A: Using ngrok (Recommended for local testing)

1. **Install ngrok** from [ngrok.com](https://ngrok.com)

2. **Start your Flask server:**
```bash
make dev
# Or: flask --app src/server/app run --debug
```

3. **In a new terminal, start ngrok:**
```bash
ngrok http 5000
```

4. **Copy the HTTPS URL** from ngrok (e.g., `https://abc123.ngrok.io`)

5. **Set the webhook** (in another terminal):
```bash
curl -X POST http://localhost:5000/webhook/set \
  -H "Content-Type: application/json" \
  -d '{"url": "https://abc123.ngrok.io/webhook"}'
```

6. **Test your bot!** Open Telegram and send `/start` to your bot

#### Option B: Direct API call to set webhook

```bash
# Replace <YOUR_BOT_TOKEN> and <YOUR_NGROK_URL>
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
  -d "url=<YOUR_NGROK_URL>/webhook"
```

### Step 5: Test the Bot

Open your bot in Telegram and try these commands:

- `/start` - Get welcome message
- `/menu` - See available features
- `/help` - Get help information
- Send any text message to chat with the bot

## 📋 Available Commands

### Makefile Commands

```bash
make dev      # Run with Flask development server (auto-reload)
make run      # Alias for 'make dev'
make prod     # Run with Gunicorn (production)
make test     # Run tests
make install  # Install dependencies
make clean    # Clean cache files
make help     # Show all commands
```

### Bot Commands (in Telegram)

- `/start` - Welcome message and introduction
- `/menu` - Show all available features
- `/help` - Get help and support

## 🔍 Verify Everything is Working

### Check server health:
```bash
curl http://localhost:5000/health
```

### Check webhook status:
```bash
curl http://localhost:5000/webhook/info
```

### View logs:
The server logs all incoming messages in JSON format to the terminal.

## 🐛 Troubleshooting

### Bot not responding?

1. **Check if webhook is set:**
```bash
curl http://localhost:5000/webhook/info
```

2. **Check server logs** - Look for incoming updates in the terminal

3. **Verify bot token** - Make sure it's correct in `.env`

4. **Check ngrok** - Make sure it's still running and the URL hasn't changed

### "Bot not configured" error?

- Make sure `TELEGRAM_BOT_TOKEN` is set in `.env`
- Restart the Flask server after changing `.env`

### Webhook errors?

- Telegram requires HTTPS - use ngrok for local development
- Make sure the webhook URL is accessible from the internet
- Check that the URL ends with `/webhook`

## 📚 Next Steps

1. **Explore the code:**
   - `src/core/bot.py` - Bot logic and command handlers
   - `src/server/app.py` - Flask webhook server

2. **Add features:**
   - Implement AI conversations in `src/dialogue/`
   - Add image generation in `src/images/`
   - Create quest system in `src/quests/`

3. **Deploy to production:**
   - See README.md for production deployment instructions
   - Use `make prod` to run with Gunicorn

## 🎯 Production Deployment

For production, you'll need:

1. A server with a public IP or domain
2. HTTPS certificate (Let's Encrypt recommended)
3. Set `WEBHOOK_URL` in `.env` to your production URL

```bash
# In .env
WEBHOOK_URL=https://your-domain.com/webhook

# Run with Gunicorn
make prod
```

## 💡 Tips

- **Development:** Use `make dev` for auto-reload on code changes
- **Logs:** All Telegram messages are logged in JSON format
- **Testing:** Use the test script: `python test_bot_structure.py`
- **Webhook:** Remember to update webhook URL if ngrok URL changes

## 🆘 Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Review the code comments in `src/core/bot.py` and `src/server/app.py`
- Check Flask logs for error messages
- Verify webhook status with `/webhook/info` endpoint

---

**Happy coding! 🚀**

