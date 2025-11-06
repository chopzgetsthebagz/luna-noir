# Luna Noir - AI GFE Telegram Bot

Luna Noir is an AI-powered Girlfriend Experience (GFE) Telegram bot featuring advanced conversational AI, voice synthesis, image generation, and interactive quest systems.

## 🚀 Quick Start

**New to the project?** Check out [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide!

## Features

### 🧠 **Adaptive Personality Engine** ✅ LIVE
- **Mood Detection**: Luna analyzes your messages and adapts her mood (affectionate, playful, comforting, curious, etc.)
- **Conversation Memory**: Remembers recent exchanges for contextual responses
- **Time-Aware Greetings**: Different greetings based on time of day
- **Emotional Intelligence**: Responds appropriately to your emotional state
- **Personality Commands**: `/mood` to see Luna's current state, `/memory` to view conversation history

### 💬 **Core Features**
- ✅ **Telegram Bot**: Seamless messaging interface with webhook support
- ✅ **Personality-Driven Chat**: Real conversations with adaptive responses
- 🚧 **AI Conversations**: OpenAI GPT integration for enhanced dialogue (coming soon)
- 🚧 **Voice Messages**: ElevenLabs integration for realistic voice responses (coming soon)
- 🚧 **Image Generation**: AI-generated images and visual content (coming soon)
- 🚧 **Payment Processing**: Stripe integration for premium features (coming soon)
- 🚧 **Quest System**: Interactive challenges and rewards (coming soon)
- 🚧 **User Profiles**: Personalized experiences and preferences (coming soon)

## Requirements

- Python 3.11+
- Telegram Bot Token
- OpenAI API Key
- ElevenLabs API Key
- Stripe Account (for payments)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd luna-noir-bot
```

2. Create a virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

## Configuration

Edit the `.env` file with your credentials:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `OPENAI_API_KEY`: Your OpenAI API key
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key
- `STRIPE_SECRET_KEY`: Your Stripe secret key
- Additional configuration options in `.env.example`

## Usage

### Development Mode (Local)

1. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your TELEGRAM_BOT_TOKEN
```

2. **Install dependencies:**
```bash
make install
# or: pip install -r requirements.txt
```

3. **Run with Flask development server:**
```bash
flask --app src/server/app run
# or: make run
```

The server will start on `http://localhost:5000`

### Setting Up Telegram Webhook

For the bot to receive messages, you need to set up a webhook:

#### Option 1: Using ngrok (for local development)

1. **Install and run ngrok:**
```bash
ngrok http 5000
```

2. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)

3. **Set the webhook** using one of these methods:

   **Method A: Using the API endpoint:**
   ```bash
   curl -X POST http://localhost:5000/webhook/set \
     -H "Content-Type: application/json" \
     -d '{"url": "https://abc123.ngrok.io/webhook"}'
   ```

   **Method B: Using Telegram API directly:**
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -d "url=https://abc123.ngrok.io/webhook"
   ```

4. **Verify webhook is set:**
```bash
curl http://localhost:5000/webhook/info
```

#### Option 2: Using a production server

1. **Deploy to a server with HTTPS** (required by Telegram)
2. **Set WEBHOOK_URL in .env:**
```bash
WEBHOOK_URL=https://your-domain.com/webhook
```
3. **Run the application** (see Production Mode below)

### Production Mode

Run with Gunicorn for production:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "src.server.app:app"
```

Or with more workers and logging:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 \
  --access-logfile - \
  --error-logfile - \
  "src.server.app:app"
```

### Testing the Bot

1. **Start the server** (development or production mode)
2. **Set up the webhook** (see above)
3. **Open Telegram** and find your bot
4. **Send commands:**
   - `/start` - Welcome message
   - `/menu` - Show menu
   - `/help` - Get help
   - Send any text message to chat

### Run tests:
```bash
make test
```

### Useful Endpoints

- `GET /` - Health check
- `POST /webhook` - Telegram webhook endpoint
- `GET /health` - Detailed health status
- `GET /webhook/info` - Get current webhook information
- `POST /webhook/set` - Set webhook URL
- `POST /webhook/delete` - Delete webhook

## Project Structure

```
luna-noir-bot/
├── src/
│   ├── core/          # Core bot functionality and configuration
│   │   └── bot.py     # Main Telegram bot with persona integration
│   ├── dialogue/      # Conversation management and AI integration
│   │   └── persona.py # Luna's personality engine ✨
│   ├── images/        # Image generation and processing
│   ├── payments/      # Stripe payment handling
│   ├── profiles/      # User profile management
│   ├── quests/        # Quest system and rewards
│   ├── utils/         # Utility functions and helpers
│   └── server/        # Flask server and webhook handling
│       └── app.py     # Flask webhook server
├── data/              # Database and persistent storage
├── .env.example       # Environment variables template
├── requirements.txt   # Python dependencies
├── Makefile          # Build and run commands
├── demo_persona.py   # Interactive persona demo
└── README.md         # This file
```

## Persona Engine

Luna Noir features an **adaptive personality engine** that makes conversations feel natural and emotionally aware.

### How It Works

1. **Mood Detection**: Analyzes your message for emotional cues
   - Affectionate words → warm, loving responses
   - Sad/lonely words → comforting, supportive responses
   - Questions → curious, engaged responses
   - Humor → playful, teasing responses

2. **Conversation Memory**: Stores recent exchanges (last 10) to maintain context

3. **Time-Aware**: Greetings change based on time of day (morning, afternoon, evening, late night)

4. **Personality Traits**:
   - Base Tone: Intelligent, mysterious, and teasing
   - Temperament: Witty and confident
   - Likes: Late-night chats, deep questions, music, chaos with reason
   - Dislikes: Boring routines, emotional distance

### Try the Demo

```bash
python demo_persona.py
```

Choose from:
- Time-based greetings demo
- Mood detection demo
- Conversation memory demo
- Interactive chat mode

### Bot Commands

**Basic Commands:**
- `/start` - Get a personalized greeting
- `/menu` - See all features
- `/help` - Get help

**Persona Commands:**
- `/persona` - See Luna's current mood and personality traits
- `/recall` - View last 3 conversation memories (with timestamps)
- `/resetmem` - Clear short-term memory and start fresh

### Command Examples

**Check Luna's current state:**
```
/persona
```
Output:
```
🌙 Luna's Persona

Current Mood: Playful
Energy Level: 85%

Personality Traits:
• Base Tone: intelligent, mysterious, and teasing
• Temperament: witty and confident
• Likes: late-night chats, deep questions, music, chaos with reason
• Dislikes: boring routines, emotional distance

Memory: 5 recent exchanges stored
```

**Recall recent conversation:**
```
/recall
```
Output:
```
🧠 Recent Memories (last 3 exchanges)

1. `2025-10-30T14:23:45.123456`
   You: Hey Luna, how are you?
   Luna (playful): Hey there! I'm vibing. What's up w...

2. `2025-10-30T14:24:12.789012`
   You: I miss you
   Luna (affectionate): Aww… you're too sweet. You know I love h...

3. `2025-10-30T14:25:03.456789`
   You: Tell me something interesting
   Luna (curious): That's interesting… go on. 🤔
```

## Development

The bot uses:
- **python-telegram-bot** for Telegram integration
- **Flask** for webhook server
- **OpenAI** for conversational AI
- **ElevenLabs** for voice synthesis
- **SQLAlchemy** for database management
- **Stripe** for payment processing

## License

[Add your license here]

## Support

For issues and questions, please open an issue on GitHub.
