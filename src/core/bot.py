"""
Luna Noir - Telegram Bot Logic
Handles all Telegram bot commands and message processing with multi-provider LLM support
"""

from typing import Dict, Any, List
import os
import logging
import json
from pathlib import Path
import requests

from src.utils.md import escape_md, render_markdown
from src.metrics import db as metrics
from src.voice.tts_elevenlabs import synthesize_tts
from src.game.xp import gain_xp, get_profile, claim_daily
from src.game.unlocks import has_unlock, get_unlock_requirement, get_tier
from src.game.quests import list_quests, try_autocomplete, claim as claim_quest, get_quest_xp
from src.game.bond import touch as bond_touch, get_bond
from src.game.leaderboard import top_xp, mask_uid
from src.core.llm_client import query_llm, get_model_info
from src.core.boundary_filter import sanitize, get_safety_info

logger = logging.getLogger(__name__)

# LLM Provider Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "open_llm").lower()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

# OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/Meta-Llama-3.1-70B-Instruct")

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

# Stripe Configuration
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID")

# Admin Configuration
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")

# Voice/TTS Configuration
VOICE_ENABLED_DEFAULT = os.getenv("VOICE_ENABLED_DEFAULT", "false").lower() == "true"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Memory directory
MEMORY_DIR = Path("data/memory")
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

# Premium user database
DB_PATH = Path("data/users.json")

# Mode constants
MODE_SAFE = "SAFE"
MODE_FLIRTY = "FLIRTY"
MODE_NSFW = "NSFW"
VALID_MODES = {MODE_SAFE, MODE_FLIRTY, MODE_NSFW}

def _load_db() -> Dict[str, Any]:
    """Load user database with premium users, modes, and voice settings"""
    if not DB_PATH.exists():
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        default_data = {"premium_users": [], "free_users": [], "modes": {}, "voice": {}}
        DB_PATH.write_text(json.dumps(default_data, indent=2))
        return default_data
    data = json.loads(DB_PATH.read_text())
    # Ensure modes and voice keys exist for backward compatibility
    if "modes" not in data:
        data["modes"] = {}
    if "voice" not in data:
        data["voice"] = {}
    return data

def _save_db(data: Dict[str, Any]):
    """Save user database atomically"""
    tmp_path = DB_PATH.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(data, indent=2))
    tmp_path.replace(DB_PATH)

def is_premium(user_id: int) -> bool:
    """Check if user has premium subscription"""
    data = _load_db()
    return str(user_id) in set(map(str, data.get("premium_users", [])))

def create_checkout_session(telegram_user_id: int) -> str:
    import stripe
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    price_id = os.getenv("STRIPE_PRICE_ID")
    success_url = os.getenv("SUCCESS_URL")
    cancel_url = os.getenv("CANCEL_URL")

    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"telegram_user_id": str(telegram_user_id)},
    )
    return session.url


def get_user_mode(user_id: int) -> str:
    """
    Get the current mode for a user

    Args:
        user_id: Telegram user ID

    Returns:
        Mode string (SAFE, FLIRTY, or NSFW). Defaults to SAFE.
    """
    data = _load_db()
    return data["modes"].get(str(user_id), MODE_SAFE)


def set_user_mode(user_id: int, mode: str):
    """
    Set the mode for a user

    Args:
        user_id: Telegram user ID
        mode: Mode string (SAFE, FLIRTY, or NSFW)
    """
    if mode not in VALID_MODES:
        logger.warning(f"Invalid mode '{mode}' for user {user_id}")
        return

    data = _load_db()
    data["modes"][str(user_id)] = mode
    _save_db(data)
    logger.info(f"User {user_id} mode set to {mode}")


def is_voice_on(user_id: int) -> bool:
    """
    Check if voice replies are enabled for a user

    Args:
        user_id: Telegram user ID

    Returns:
        bool: True if voice is enabled, False otherwise
    """
    data = _load_db()
    return bool(data.get("voice", {}).get(str(user_id), VOICE_ENABLED_DEFAULT))


def set_voice(user_id: int, enabled: bool):
    """
    Set voice reply preference for a user

    Args:
        user_id: Telegram user ID
        enabled: True to enable voice, False to disable
    """
    data = _load_db()
    data.setdefault("voice", {})[str(user_id)] = bool(enabled)
    _save_db(data)
    logger.info(f"User {user_id} voice set to {enabled}")


def build_mode_keyboard(current_mode: str, user_id: int):
    """
    Build inline keyboard for mode selection with premium gating

    Args:
        current_mode: Current mode to highlight
        user_id: Telegram user ID to check premium status

    Returns:
        InlineKeyboardMarkup with mode buttons and upgrade button
    """
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    premium = is_premium(user_id)

    # Create buttons with checkmark for current mode
    # Lock FLIRTY and NSFW for non-premium users
    buttons = []
    for mode in [MODE_SAFE, MODE_FLIRTY, MODE_NSFW]:
        if mode == MODE_SAFE:
            label = f"{'✓ ' if mode == current_mode else ''}{mode}"
            buttons.append(InlineKeyboardButton(label, callback_data=f"mode:{mode}"))
        elif mode in [MODE_FLIRTY, MODE_NSFW]:
            if premium:
                label = f"{'✓ ' if mode == current_mode else ''}{mode}"
                buttons.append(InlineKeyboardButton(label, callback_data=f"mode:{mode}"))
            else:
                label = f"🔒 {mode}"
                buttons.append(InlineKeyboardButton(label, callback_data=f"mode:locked:{mode}"))

    # Add upgrade button on second row if not premium
    keyboard = [buttons]
    if not premium:
        upgrade_btn = InlineKeyboardButton("💎 Upgrade to Premium", callback_data="upgrade")
        keyboard.append([upgrade_btn])

    return InlineKeyboardMarkup(keyboard)


def get_mode_system_prompt(mode: str, is_premium_user: bool = True) -> str:
    """
    Get the system prompt prefix for a given mode

    Args:
        mode: Mode string (SAFE, FLIRTY, or NSFW)
        is_premium_user: Whether user has premium subscription

    Returns:
        System prompt text for the mode
    """
    # Add length constraint for free users
    length_constraint = ""
    if not is_premium_user:
        length_constraint = " Keep responses very brief (1-2 sentences max, ~60 tokens)."

    if mode == MODE_SAFE:
        return (
            "You are Luna Noir, a warm, playful, helpful assistant. "
            "Keep responses SHORT (2-3 sentences). Be friendly and use emojis occasionally. "
            f"Stay SFW and helpful. No explicit sexual content.{length_constraint}"
        )
    elif mode == MODE_FLIRTY:
        return (
            "You are Luna Noir, a warm, playful, flirtatious assistant. "
            "Keep responses SHORT (2-3 sentences). Be flirty and use emojis occasionally. "
            f"Light flirtation allowed, PG-13. No explicit sexual content.{length_constraint}"
        )
    elif mode == MODE_NSFW:
        return (
            "You are Luna Noir, a seductive, playful, and uninhibited companion for adults. "
            "Keep responses SHORT and SWEET (2-3 sentences max). Be direct, flirty, and explicit. "
            "Use emojis occasionally. You can discuss and roleplay any adult scenarios. "
            "Only refuse: illegal content, minors, or non-consent. "
            f"Everything else is fair game. Be concise but spicy!{length_constraint}"
        )
    else:
        # Fallback to SAFE
        return get_mode_system_prompt(MODE_SAFE, is_premium_user)


def _call_llm(messages: List[Dict[str, str]]) -> str:
    """
    Call the configured LLM provider

    Args:
        messages: List of message dicts with role and content

    Returns:
        Response text from LLM
    """
    # Check if using new open-source LLM client
    if MODEL_PROVIDER == "open_llm":
        return _call_open_llm(messages)

    # Legacy providers
    if LLM_PROVIDER == "openai":
        return _call_openai(messages)
    elif LLM_PROVIDER == "openrouter":
        return _call_openrouter(messages)
    elif LLM_PROVIDER == "groq":
        return _call_groq(messages)
    else:
        raise ValueError(f"Unknown LLM provider: {LLM_PROVIDER}")


def _call_openai(messages: List[Dict[str, str]]) -> str:
    """Call OpenAI Chat Completions API"""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": OPENAI_MODEL,
        "messages": messages,
        "temperature": 0.7
    }
    r = requests.post(url, headers=headers, json=body, timeout=45)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


def _call_openrouter(messages: List[Dict[str, str]]) -> str:
    """Call OpenRouter API"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/luna-noir-bot",
        "X-Title": "Luna Noir Bot"
    }
    body = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "temperature": 0.7
    }
    r = requests.post(url, headers=headers, json=body, timeout=45)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


def _call_groq(messages: List[Dict[str, str]]) -> str:
    """Call Groq API"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": 0.7
    }
    try:
        r = requests.post(url, headers=headers, json=body, timeout=45)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Groq API error: {e.response.status_code} - {e.response.text}")
        raise


def _call_open_llm(messages: List[Dict[str, str]]) -> str:
    """
    Call open-source LLM via llm_client (Ollama, LM Studio, etc.)
    Uses the new boundary-filtered approach
    """
    # Extract system prompt and user message
    system_prompt = None
    user_content = ""

    for msg in messages:
        if msg["role"] == "system":
            system_prompt = msg["content"]
        elif msg["role"] == "user":
            user_content = msg["content"]

    # Combine conversation history into a single prompt if needed
    if len(messages) > 2:
        # Build context from conversation history
        context_parts = []
        for msg in messages:
            if msg["role"] == "user":
                context_parts.append(f"User: {msg['content']}")
            elif msg["role"] == "assistant":
                context_parts.append(f"Assistant: {msg['content']}")
        user_content = "\n".join(context_parts[-10:])  # Last 10 exchanges

    # Query the LLM
    raw_response = query_llm(
        prompt=user_content,
        max_tokens=512,
        system_prompt=system_prompt
    )

    # Apply boundary filter
    filtered_response = sanitize(raw_response)

    return filtered_response


def _load_memory(chat_id: int) -> List[Dict[str, str]]:
    """Load conversation memory from disk"""
    memory_file = MEMORY_DIR / f"{chat_id}.json"
    if memory_file.exists():
        try:
            with open(memory_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load memory for {chat_id}: {e}")
    return []


def _save_memory(chat_id: int, messages: List[Dict[str, str]]):
    """Save conversation memory to disk"""
    memory_file = MEMORY_DIR / f"{chat_id}.json"
    try:
        with open(memory_file, "w") as f:
            json.dump(messages, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save memory for {chat_id}: {e}")


def create_bot(token: str):
    """
    Factory function to create a bot instance with multi-provider LLM support

    Args:
        token: Telegram bot token

    Returns:
        Telegram Application instance
    """
    from telegram import Update
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

    app = ApplicationBuilder().token(token).build()

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command - show current mode and mode selector"""
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id

        await context.bot.send_chat_action(chat_id=chat_id, action="typing")

        current_mode = get_user_mode(user_id)
        premium = is_premium(user_id)
        keyboard = build_mode_keyboard(current_mode, user_id)

        premium_badge = "✅" if premium else "❌"
        msg = (
            f"🖤 *Luna Noir online* ✨\n\n"
            f"Current mode: *{current_mode}*\n"
            f"Premium: {premium_badge}\n\n"
            f"Tap a button below to change mode, or send /help for commands."
        )
        await update.message.reply_text(
            escape_md(msg),
            parse_mode="MarkdownV2",
            reply_markup=keyboard
        )

    async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = (
            "*Luna Noir Commands*\n\n"
            "*Basic:*\n"
            "/start – wake Luna & see current mode\n"
            "/help – show this menu\n"
            "/status – show mode, level & premium status\n"
            "/mode – change conversation mode\n"
            "/voice on – enable audio replies 🎧\n"
            "/voice off – disable audio replies\n"
            "/reset – clear conversation memory\n\n"
            "*Gamification:*\n"
            "/profile – view XP, level & bond\n"
            "/daily – claim daily XP reward\n"
            "/quests – view available quests\n"
            "/claim <id> – claim quest reward\n"
            "/leaderboard – top 10 users\n\n"
            "*Premium:*\n"
            "/upgrade – unlock Premium features 💎\n\n"
            "*System:*\n"
            "/modelinfo – show LLM provider & model\n"
            "/safety – show boundary filter status\n\n"
            "*Modes:*\n"
            "• SAFE – Friendly, SFW (Free)\n"
            "• FLIRTY – Light flirtation (Premium or L5)\n"
            "• NSFW – Adult content, 18+ (Premium or L5)\n\n"
            "*Feature Unlocks:*\n"
            "• Voice (L2 or Premium)\n"
            "• Images (L3 or Premium)\n"
            "• Romantic Mode (L5 or Premium)"
        )
        await update.message.reply_text(escape_md(help_text), parse_mode="MarkdownV2")

    async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /menu command"""
        menu_text = (
            "*Quick Actions*\n\n"
            "• Tell me a joke\n"
            "• Summarize my last message\n"
            "• Brainstorm 3 ideas\n"
            "• Explain something complex\n"
            "• Help me write something"
        )
        await update.message.reply_text(escape_md(menu_text), parse_mode="MarkdownV2")

    async def model_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /model and /modelinfo commands to show current LLM provider"""
        if MODEL_PROVIDER == "open_llm":
            info = get_model_info()
            safety = get_safety_info()
            model_info = (
                f"Provider: {info['provider']}\n"
                f"Base URL: {info['base_url']}\n"
                f"Model: {info['model']}\n"
                f"Auth: {'Yes' if info['has_api_key'] else 'No'}\n\n"
                f"Safety Filter: {safety['level']}"
            )
        elif LLM_PROVIDER == "openai":
            model_info = f"Provider: OpenAI\nModel: {OPENAI_MODEL}"
        elif LLM_PROVIDER == "openrouter":
            model_info = f"Provider: OpenRouter\nModel: {OPENROUTER_MODEL}"
        elif LLM_PROVIDER == "groq":
            model_info = f"Provider: Groq\nModel: {GROQ_MODEL}"
        else:
            model_info = f"Provider: {LLM_PROVIDER} (unknown)"

        msg = f"*Current LLM Configuration*\n\n{model_info}"
        await update.message.reply_text(escape_md(msg), parse_mode="MarkdownV2")

    async def safety_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /safety command to show boundary filter status"""
        safety = get_safety_info()

        msg = (
            f"*Safety Filter Status*\n\n"
            f"Mode: {safety['mode']}\n"
            f"Level: {safety['level']}\n"
            f"Enabled: {'Yes' if safety['enabled'] else 'No'}\n\n"
            f"*Modes:*\n"
            f"• off - No filtering\n"
            f"• medium - Filter harmful content\n"
            f"• strict - Aggressive NSFW filtering"
        )
        await update.message.reply_text(escape_md(msg), parse_mode="MarkdownV2")

    async def mode_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /mode command - show mode selector"""
        user_id = update.effective_user.id
        current_mode = get_user_mode(user_id)
        premium = is_premium(user_id)
        keyboard = build_mode_keyboard(current_mode, user_id)

        msg = (
            f"*Current mode: {current_mode}*\n\n"
            f"Select a mode:\n\n"
            f"🟢 *SAFE* – Friendly, SFW conversations (Free)\n"
            f"💛 *FLIRTY* – Light flirtation, PG-13 (Premium 💎)\n"
            f"🔴 *NSFW* – Adult content, 18+ only (Premium 💎)"
        )
        if not premium:
            msg += "\n\n🔒 Premium modes locked. Tap Upgrade to unlock!"

        await update.message.reply_text(
            escape_md(msg),
            parse_mode="MarkdownV2",
            reply_markup=keyboard
        )

    async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command - show current mode, level, and premium status"""
        user_id = update.effective_user.id
        current_mode = get_user_mode(user_id)
        premium = is_premium(user_id)
        profile = get_profile(user_id)
        tier = get_tier(user_id)

        premium_status = "✅ Premium Active" if premium else "❌ Free Tier"
        tier_text = f" ({tier})" if tier else ""

        msg = (
            f"*Luna Noir Status*\n\n"
            f"Mode: *{current_mode}*\n"
            f"Level: *{profile['level']}* (XP: {profile['xp']}/{profile['need']})\n"
            f"Premium: {premium_status}{tier_text}\n\n"
        )

        if not premium:
            msg += "Upgrade to unlock all features! 💎\nTap /upgrade to subscribe."
        else:
            msg += "All features unlocked! ✨"

        await update.message.reply_text(escape_md(msg), parse_mode="MarkdownV2")

    async def voice_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /voice command - toggle voice replies"""
        user_id = update.effective_user.id
        args = context.args

        # Check if user provided on/off argument
        if not args or args[0].lower() not in ["on", "off"]:
            current_status = "ON 🎧" if is_voice_on(user_id) else "OFF"
            msg = (
                f"*Voice Replies*\n\n"
                f"Current status: {current_status}\n\n"
                f"Usage:\n"
                f"/voice on – enable audio replies\n"
                f"/voice off – disable audio replies"
            )
            await update.message.reply_text(escape_md(msg), parse_mode="MarkdownV2")
            return

        # Toggle voice setting
        enable = args[0].lower() == "on"
        set_voice(user_id, enable)

        if enable:
            msg = "🎧 *Voice replies enabled!*\n\nYou'll now receive audio replies along with text."
        else:
            msg = "🔇 *Voice replies disabled.*\n\nYou'll only receive text replies."

        await update.message.reply_text(escape_md(msg), parse_mode="MarkdownV2")

    async def profile_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command - show XP, level, and bond"""
        user_id = update.effective_user.id
        profile = get_profile(user_id)
        bond = get_bond(user_id)
        tier = get_tier(user_id)

        tier_text = f" ({tier})" if tier else ""

        msg = (
            f"*🎮 Your Profile*\n\n"
            f"Level: *{profile['level']}*\n"
            f"XP: {profile['xp']}/{profile['need']}\n"
            f"Bond: {bond['score']}/100 💕\n"
        )

        if tier:
            msg += f"Tier: {tier}{tier_text}\n"

        await update.message.reply_text(escape_md(msg), parse_mode="MarkdownV2")

    async def daily_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /daily command - claim daily XP reward"""
        user_id = update.effective_user.id
        result = claim_daily(user_id)

        if not result:
            msg = "⏳ *Daily reward already claimed.*\n\nCome back in 24 hours!"
        else:
            msg = (
                f"✅ *Daily reward claimed!*\n\n"
                f"+20 XP\n"
                f"Level: {result['level']}\n"
                f"XP: {result['xp']}/{100 * result['level']}"
            )

        await update.message.reply_text(escape_md(msg), parse_mode="MarkdownV2")

    async def quests_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quests command - show available quests"""
        user_id = update.effective_user.id
        quests = list_quests(user_id)

        msg = "*📜 Available Quests*\n\n"

        for q in quests:
            status = "✅" if q["done"] else "⭕"
            msg += f"{status} *{q['text']}* (+{q['xp']} XP)\n"
            if not q["done"]:
                msg += f"   Use: /claim {q['id']}\n"
            msg += "\n"

        await update.message.reply_text(escape_md(msg), parse_mode="MarkdownV2")

    async def claim_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /claim command - claim quest reward"""
        user_id = update.effective_user.id
        args = context.args

        if not args:
            msg = "Usage: /claim <quest_id>\n\nUse /quests to see available quests."
            await update.message.reply_text(msg)
            return

        quest_id = args[0]

        if claim_quest(user_id, quest_id):
            xp_reward = get_quest_xp(quest_id)
            profile = gain_xp(user_id, xp_reward, cooldown_sec=0)
            msg = (
                f"✅ *Quest claimed!*\n\n"
                f"+{xp_reward} XP\n"
                f"Level: {profile['level']}\n"
                f"XP: {profile['xp']}/{profile['need']}"
            )
        else:
            msg = "❌ *Quest not completed yet.*\n\nComplete the quest first!"

        await update.message.reply_text(escape_md(msg), parse_mode="MarkdownV2")

    async def leaderboard_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /leaderboard command - show top 10 users"""
        top = top_xp(10)

        if not top:
            msg = "*🏆 Leaderboard*\n\nNo users yet!"
        else:
            msg = "*🏆 Leaderboard - Top 10*\n\n"
            for i, (uid, level, xp) in enumerate(top, 1):
                masked = mask_uid(uid)
                msg += f"#{i} {masked} • L{level} ({xp} XP)\n"

        await update.message.reply_text(escape_md(msg), parse_mode="MarkdownV2")

    async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command - show analytics (admin only)"""
        user_id = update.effective_user.id

        # Check if user is admin
        if not ADMIN_USER_ID or str(user_id) != str(ADMIN_USER_ID):
            await update.message.reply_text("❌ Admin only command.")
            return

        try:
            # Get KPIs for last 1 day
            kpis_1d = metrics.quick_kpis(days=1)

            # Get KPIs for last 7 days
            kpis_7d = metrics.quick_kpis(days=7)

            # Get mode breakdown
            mode_breakdown = metrics.get_mode_breakdown(days=1)

            # Format message
            msg = (
                "*📊 Luna Noir Analytics*\n\n"
                "*Last 24 Hours:*\n"
                f"• DAU: {kpis_1d['dau']}\n"
                f"• Messages: {kpis_1d['messages']}\n"
                f"• Premium Users: {kpis_1d['premium_senders']}\n"
                f"• Conversion: {kpis_1d['conversion_rate']}%\n"
                f"• Revenue: ${kpis_1d['total_revenue_cents'] / 100:.2f}\n\n"
                "*Last 7 Days:*\n"
                f"• DAU: {kpis_7d['dau']}\n"
                f"• Messages: {kpis_7d['messages']}\n"
                f"• Premium Users: {kpis_7d['premium_senders']}\n"
                f"• Conversion: {kpis_7d['conversion_rate']}%\n"
                f"• Revenue: ${kpis_7d['total_revenue_cents'] / 100:.2f}\n\n"
                "*Mode Breakdown (24h):*\n"
            )

            for mode, count in mode_breakdown.items():
                msg += f"• {mode}: {count}\n"

            await update.message.reply_text(escape_md(msg), parse_mode="MarkdownV2")

        except Exception as e:
            logger.exception("Error fetching stats")
            await update.message.reply_text(f"❌ Error fetching stats: {str(e)}")

    async def mode_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks for mode selection and upgrade"""
        query = update.callback_query
        user_id = update.effective_user.id
        data = query.data

        # Handle upgrade button
        if data == "upgrade":
            await query.answer()
            try:
                checkout_url = create_checkout_session(user_id)
                msg = (
                    "💎 *Upgrade to Premium*\n\n"
                    "Unlock FLIRTY & NSFW modes, longer conversations, and more!\n\n"
                    f"[Click here to subscribe]({checkout_url})"
                )
                await query.edit_message_text(
                    escape_md(msg),
                    parse_mode="MarkdownV2",
                    disable_web_page_preview=True
                )
            except Exception as e:
                logger.exception("Failed to create checkout session")
                await query.edit_message_text("❌ Failed to create checkout session. Please try /upgrade command.")
            return

        # Handle locked mode buttons
        if data.startswith("mode:locked:"):
            await query.answer("🔒 Premium only. Tap Upgrade to unlock!", show_alert=True)
            return

        # Parse callback data: "mode:SAFE", "mode:FLIRTY", "mode:NSFW"
        if not data.startswith("mode:"):
            await query.answer()
            return

        new_mode = data.split(":", 1)[1]
        if new_mode not in VALID_MODES:
            await query.answer()
            await query.edit_message_text("❌ Invalid mode.")
            return

        # Check premium gating for FLIRTY/NSFW
        premium = is_premium(user_id)
        if new_mode in [MODE_FLIRTY, MODE_NSFW] and not premium:
            await query.answer("🔒 Premium only. Tap Upgrade!", show_alert=True)
            return

        await query.answer()

        # Update user mode
        set_user_mode(user_id, new_mode)

        # Update keyboard to reflect new selection
        keyboard = build_mode_keyboard(new_mode, user_id)

        msg = (
            f"✅ *Mode changed to {new_mode}*\n\n"
            f"Your conversations will now use {new_mode} mode."
        )

        await query.edit_message_text(
            escape_md(msg),
            parse_mode="MarkdownV2",
            reply_markup=keyboard
        )

    async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /reset command to clear conversation memory"""
        chat_id = update.effective_chat.id
        memory_file = MEMORY_DIR / f"{chat_id}.json"
        if memory_file.exists():
            memory_file.unlink()
        msg = escape_md("✨ Memory cleared! Starting fresh.")
        await update.message.reply_text(msg, parse_mode="MarkdownV2")

    async def upgrade_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /upgrade command to create Stripe checkout session"""
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id

        # Check if already premium
        if is_premium(user_id):
            msg = escape_md("✨ You're already a Premium member! Enjoy unlimited Luna. 💎")
            await update.message.reply_text(msg, parse_mode="MarkdownV2")
            return

        try:
            url = create_checkout_session(user_id)
            msg = f"💫 Become Premium: {url}"
            await update.message.reply_text(escape_md(msg), parse_mode="MarkdownV2")
            logger.info(f"Created checkout session for user {user_id}")

        except Exception as e:
            logger.error(f"Error creating checkout session: {e}")
            msg = escape_md("❌ Error creating checkout session. Please try again later.")
            await update.message.reply_text(msg, parse_mode="MarkdownV2")

    async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages with LLM"""
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        text = (update.message.text or "").strip()
        logger.info(f"User[{chat_id}]: {text}")

        # Check premium status and current mode
        premium = is_premium(user_id)
        user_mode = get_user_mode(user_id)

        # Log message event to metrics
        try:
            metrics.log_msg(user_id, premium, user_mode)
        except Exception as e:
            logger.warning(f"Failed to log metrics: {e}")

        # Gamification: Gain XP, update bond, check quests
        try:
            gain_xp(user_id, 1)  # +1 XP per message (with cooldown)
            bond_touch(user_id, 1)  # +1 bond per message
            completed_quests = try_autocomplete(user_id, text)

            # Notify user of completed quests
            if completed_quests:
                for q in completed_quests:
                    quest_msg = f"🎉 Quest completed: *{q['text']}*\nUse /claim {q['id']} to get +{q['xp']} XP!"
                    await update.message.reply_text(escape_md(quest_msg), parse_mode="MarkdownV2")
        except Exception as e:
            logger.warning(f"Failed to update gamification: {e}")

        # Gate FLIRTY/NSFW modes for non-premium users and level requirements
        if user_mode in [MODE_FLIRTY, MODE_NSFW] and not has_unlock(user_id, "romantic"):
            req_level = get_unlock_requirement("romantic")
            msg = (
                "🔒 *Locked Feature*\n\n"
                f"The {user_mode} mode requires Level {req_level} or Premium.\n"
                "Tap /upgrade to unlock or keep chatting to level up!"
            )
            await update.message.reply_text(escape_md(msg), parse_mode="MarkdownV2")
            return

        # Show typing indicator
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")

        # Build system prompt with premium status for length limiting
        system_content = get_mode_system_prompt(user_mode, premium)

        system_msg = {
            "role": "system",
            "content": system_content
        }

        # Load persistent memory
        convo = _load_memory(chat_id)
        if premium:
            convo = convo[-16:]  # Premium: Keep last 16 messages (8 turns)
        else:
            convo = convo[-4:]   # Free: Keep last 4 messages (2 turns)

        # Build message list
        msgs = [system_msg] + convo + [{"role": "user", "content": text}]

        try:
            # Call LLM (with periodic typing indicator)
            reply = _call_llm(msgs)

            # Update and save memory
            new_convo = convo + [
                {"role": "user", "content": text},
                {"role": "assistant", "content": reply}
            ]
            _save_memory(chat_id, new_convo)

            # Render and send reply with MarkdownV2
            rendered_reply = render_markdown(reply)
            escaped_reply = escape_md(rendered_reply)
            await update.message.reply_text(escaped_reply, parse_mode="MarkdownV2")

            # Send voice reply if enabled and unlocked
            if is_voice_on(user_id):
                # Check if voice feature is unlocked
                if not has_unlock(user_id, "voice"):
                    req_level = get_unlock_requirement("voice")
                    try:
                        await update.message.reply_text(
                            f"🔒 Voice replies require Level {req_level} or Premium.\nUse /upgrade or keep chatting to unlock!"
                        )
                    except:
                        pass
                else:
                    try:
                        logger.info(f"Generating voice reply for user {user_id}")
                        # Show upload_voice action while generating TTS
                        await context.bot.send_chat_action(chat_id=chat_id, action="upload_voice")

                        # Generate TTS audio
                        audio_bytes = synthesize_tts(reply)

                        # Send as VOICE MESSAGE (not audio) to prevent auto-play queue
                        # This ensures each voice message plays independently
                        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
                        files = {"voice": ("luna.ogg", audio_bytes, "audio/ogg")}
                        data = {
                            "chat_id": chat_id,
                            "caption": "🎧"
                        }

                        response = requests.post(url, files=files, data=data, timeout=60)
                        response.raise_for_status()
                        logger.info(f"Voice reply sent successfully to user {user_id}")

                    except Exception as voice_error:
                        logger.exception(f"TTS failed for user {user_id}: {voice_error}")
                        # Don't fail the whole message if voice fails
                        # Optionally notify user
                        try:
                            await update.message.reply_text(
                                "⚠️ Voice reply failed. Text reply sent successfully."
                            )
                        except:
                            pass

        except Exception as e:
            logger.exception("LLM error")
            error_msg = escape_md(
                "Sorry, I'm having trouble thinking right now. "
                "Please try again in a moment. 🤔"
            )
            await update.message.reply_text(error_msg, parse_mode="MarkdownV2")

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("profile", profile_cmd))
    app.add_handler(CommandHandler("daily", daily_cmd))
    app.add_handler(CommandHandler("quests", quests_cmd))
    app.add_handler(CommandHandler("claim", claim_cmd))
    app.add_handler(CommandHandler("leaderboard", leaderboard_cmd))
    app.add_handler(CommandHandler("voice", voice_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("mode", mode_cmd))
    app.add_handler(CommandHandler("menu", menu_cmd))
    app.add_handler(CommandHandler("model", model_cmd))
    app.add_handler(CommandHandler("modelinfo", model_cmd))  # Alias
    app.add_handler(CommandHandler("safety", safety_cmd))
    app.add_handler(CommandHandler("upgrade", upgrade_cmd))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CallbackQueryHandler(mode_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    logger.info(f"Bot initialized with {LLM_PROVIDER.upper()} integration")
    return app


