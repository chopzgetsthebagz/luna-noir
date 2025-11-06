#!/usr/bin/env python3
"""
Luna Noir – AI GFE Telegram Bot
Flask webhook server for Telegram bot with python-telegram-bot integration
"""
import os, sys, logging, asyncio
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# make src/* imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv()

from src.core.bot import create_bot
from src.payments.stripe_webhook import bp as stripe_bp

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

# Configure logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.register_blueprint(stripe_bp)

# Initialize bot application
bot_app = None
if TELEGRAM_TOKEN:
    bot_app = create_bot(TELEGRAM_TOKEN)
    logger.info("Bot initialized with Luna Noir Persona")
else:
    logger.error("TELEGRAM_TOKEN not found in environment")


@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'bot': 'Luna Noir',
        'version': '0.1.0',
        'telegram_configured': TELEGRAM_TOKEN is not None
    })


@app.get("/health")
def health():
    """Health check for Railway/monitoring"""
    return {"ok": True}, 200


@app.get("/llmtest")
def llmtest():
    """Test the LLM backend (open-source or OpenAI)"""
    try:
        from src.core.llm_client import query_llm, get_model_info
        from src.core.boundary_filter import sanitize, get_safety_info

        # Get model info
        model_info = get_model_info()
        safety_info = get_safety_info()

        # Test query
        test_prompt = "Say hello in a friendly way!"
        raw_response = query_llm(test_prompt, max_tokens=100)
        filtered_response = sanitize(raw_response)

        return jsonify({
            "status": "ok",
            "model": model_info,
            "safety": safety_info,
            "test": {
                "prompt": test_prompt,
                "raw_response": raw_response,
                "filtered_response": filtered_response
            }
        })
    except Exception as e:
        logger.exception("LLM test failed")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming webhook updates from Telegram"""
    data = request.get_json(force=True, silent=True) or {}
    print("Incoming update:", data, flush=True)  # Log request body

    if not TELEGRAM_TOKEN or not bot_app:
        logging.error("TELEGRAM_TOKEN or bot_app missing")
        # Still return 200 to Telegram to avoid retries
        return jsonify({"status": "ok"}), 200

    try:
        # Process update using python-telegram-bot
        from telegram import Update

        # Create Update object from webhook data
        update = Update.de_json(data, bot_app.bot)

        # Process the update asynchronously
        async def process():
            await bot_app.initialize()
            await bot_app.process_update(update)
            await bot_app.shutdown()

        # Run the async function
        asyncio.run(process())

        logger.info(f"✓ Processed update successfully")

    except Exception as e:
        logging.exception("Webhook error: %s", e)
        # ALWAYS return 200 to Telegram to prevent infinite retries

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5050"))
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=port,
        debug=os.getenv("FLASK_DEBUG", "False").lower() == "true"
    )

