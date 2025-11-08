"""
Strategic upsell prompts and messaging for Luna Noir bot.
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import Tuple

# ============================================================================
# UPSELL MESSAGES
# ============================================================================

def get_image_limit_reached_message(plan: str) -> Tuple[str, InlineKeyboardMarkup]:
    """Message when user hits image generation limit"""
    
    if plan == "basic":
        msg = (
            "📸 *Monthly Image Limit Reached\\!*\n\n"
            "You've used all 20 images this month on your Basic plan\\.\n\n"
            "*Upgrade to VIP for:*\n"
            "✨ UNLIMITED AI images\n"
            "✨ Custom outfit requests\n"
            "✨ Exclusive VIP scenes\n"
            "✨ Extended memory\n\n"
            "Or buy a one\\-time credit pack\\!"
        )
        
        keyboard = [
            [InlineKeyboardButton("💎 Upgrade to VIP ($19.99/mo)", callback_data="upgrade:vip")],
            [InlineKeyboardButton("🎫 Buy 20 Images ($9.99)", callback_data="buy_credits:20_pack")],
            [InlineKeyboardButton("« Back", callback_data="menu_main")]
        ]
    
    else:  # Free user
        msg = (
            "📸 *No Images Remaining\\!*\n\n"
            "You've used your free trial images\\.\n\n"
            "*Choose an option:*\n"
            "💜 Subscribe for unlimited access\n"
            "🎫 Buy one\\-time credit packs\n\n"
            "*Premium Plans:*\n"
            "• Basic: 20 images/month \\- $9\\.99\n"
            "• VIP: UNLIMITED images \\- $19\\.99\n"
            "• Ultimate: Everything \\- $49\\.99"
        )
        
        keyboard = [
            [InlineKeyboardButton("💎 See All Plans", callback_data="show_plans")],
            [
                InlineKeyboardButton("🎫 5 Images ($2.99)", callback_data="buy_credits:5_pack"),
                InlineKeyboardButton("🎫 20 Images ($9.99)", callback_data="buy_credits:20_pack")
            ],
            [InlineKeyboardButton("« Back", callback_data="menu_main")]
        ]
    
    return msg, InlineKeyboardMarkup(keyboard)


def get_free_trial_offer_message() -> Tuple[str, InlineKeyboardMarkup]:
    """Offer free trial to new users"""
    
    msg = (
        "🎁 *Welcome to Luna Noir\\!*\n\n"
        "I'd love to get to know you better\\.\\.\\. 💜\n\n"
        "*Start your FREE 3\\-day trial:*\n"
        "✅ 5 FREE AI-generated images\n"
        "✅ NSFW mode unlocked\n"
        "✅ Voice messages\n"
        "✅ No credit card required\\!\n\n"
        "After trial: Subscribe or buy credits anytime\\."
    )
    
    keyboard = [
        [InlineKeyboardButton("🎁 Start FREE Trial", callback_data="start_trial")],
        [InlineKeyboardButton("💎 See Premium Plans", callback_data="show_plans")],
        [InlineKeyboardButton("Maybe Later", callback_data="menu_main")]
    ]
    
    return msg, InlineKeyboardMarkup(keyboard)


def get_nsfw_mode_upsell_message() -> Tuple[str, InlineKeyboardMarkup]:
    """Upsell when user tries to access NSFW mode"""
    
    msg = (
        "🔒 *NSFW Mode Locked*\n\n"
        "Want to see my naughty side? 😈\n\n"
        "*Unlock with Premium:*\n"
        "🔥 Explicit conversations\n"
        "🔥 NSFW AI images\n"
        "🔥 Adult content\n"
        "🔥 No filters\n\n"
        "*Try it FREE for 3 days\\!*"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎁 Start FREE Trial", callback_data="start_trial")],
        [InlineKeyboardButton("💎 Subscribe Now", callback_data="show_plans")],
        [InlineKeyboardButton("« Back", callback_data="menu_main")]
    ]
    
    return msg, InlineKeyboardMarkup(keyboard)


def get_voice_upsell_message() -> Tuple[str, InlineKeyboardMarkup]:
    """Upsell when user tries voice messages"""
    
    msg = (
        "🔒 *Voice Messages Locked*\n\n"
        "Want to hear my voice? 🎧💜\n\n"
        "Unlock voice messages with Premium\\!\n\n"
        "*Start FREE 3\\-day trial:*\n"
        "✅ Voice messages\n"
        "✅ NSFW mode\n"
        "✅ 5 FREE images\n"
        "✅ No credit card\\!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎁 Start FREE Trial", callback_data="start_trial")],
        [InlineKeyboardButton("💎 See Plans", callback_data="show_plans")],
        [InlineKeyboardButton("« Back", callback_data="menu_main")]
    ]
    
    return msg, InlineKeyboardMarkup(keyboard)


def get_plans_comparison_message() -> Tuple[str, InlineKeyboardMarkup]:
    """Show all premium plans comparison"""
    
    msg = (
        "💎 *Premium Plans*\n\n"
        
        "*💜 BASIC - $9.99/month*\n"
        "✅ NSFW & FLIRTY modes\n"
        "✅ 20 AI images/month\n"
        "✅ Voice messages\n"
        "✅ Longer conversations\n"
        "✅ Priority support\n\n"
        
        "*💎 VIP - $19.99/month* (POPULAR)\n"
        "✅ Everything in Basic\n"
        "✅ UNLIMITED images\n"
        "✅ Custom outfits\n"
        "✅ Exclusive scenes\n"
        "✅ Extended memory\n"
        "✅ Early access\n\n"
        
        "*👑 ULTIMATE - $49.99/month*\n"
        "✅ Everything in VIP\n"
        "✅ Custom prompts\n"
        "✅ Video messages (soon)\n"
        "✅ 1-on-1 support\n"
        "✅ Request features\n"
        "✅ Credits mention\n\n"

        "🎁 *All plans: 3\\-day FREE trial\\!*"
    )
    
    keyboard = [
        [InlineKeyboardButton("💜 Basic ($9.99/mo)", callback_data="subscribe:basic")],
        [InlineKeyboardButton("💎 VIP ($19.99/mo) ⭐", callback_data="subscribe:vip")],
        [InlineKeyboardButton("👑 Ultimate ($49.99/mo)", callback_data="subscribe:ultimate")],
        [InlineKeyboardButton("🎫 Buy Credits Instead", callback_data="show_credits")],
        [InlineKeyboardButton("« Back", callback_data="menu_main")]
    ]
    
    return msg, InlineKeyboardMarkup(keyboard)


def get_credits_shop_message() -> Tuple[str, InlineKeyboardMarkup]:
    """Show credit packs for purchase"""
    
    msg = (
        "🎫 *Buy Image Credits*\n\n"
        "One\\-time purchase, no subscription\\!\n\n"
        "*Credit Packs:*\n"
        "• 5 images \\- $2\\.99\n"
        "• 20 images \\- $9\\.99\n"
        "• 50 images \\+ 10 BONUS \\- $19\\.99\n\n"
        "💡 *Tip:* VIP subscription \\($19\\.99/mo\\) gives you UNLIMITED images\\!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎫 5 Images - $2.99", callback_data="buy_credits:5_pack")],
        [InlineKeyboardButton("🎫 20 Images - $9.99", callback_data="buy_credits:20_pack")],
        [InlineKeyboardButton("🎫 50+10 Images - $19.99 (BEST VALUE)", callback_data="buy_credits:50_pack")],
        [InlineKeyboardButton("💎 Or Subscribe for Unlimited", callback_data="show_plans")],
        [InlineKeyboardButton("« Back", callback_data="menu_main")]
    ]
    
    return msg, InlineKeyboardMarkup(keyboard)


def get_trial_ending_soon_message(days_left: int, images_left: int) -> str:
    """Message when trial is ending soon"""
    
    return (
        f"⏰ *Trial Ending Soon\\!*\n\n"
        f"You have {days_left} day\\(s\\) and {images_left} image\\(s\\) left\\.\n\n"
        f"Don't lose access to:\n"
        f"🔥 NSFW mode\n"
        f"📸 AI images\n"
        f"🎧 Voice messages\n\n"
        f"Subscribe now to keep all features\\!"
    )


def get_after_image_upsell_message(images_remaining: int, plan: str) -> str:
    """Subtle upsell after generating an image"""
    
    if plan == "basic":
        return f"💜 Image generated\\! You have {images_remaining}/20 images left this month\\. Upgrade to VIP for unlimited\\!"
    elif plan is None and images_remaining > 0:
        return f"💜 Image generated\\! {images_remaining} trial images remaining\\. Subscribe to get more\\!"
    else:
        return "💜 Image generated\\! Enjoying Luna? Upgrade for unlimited images\\!"


def get_conversation_limit_message() -> Tuple[str, InlineKeyboardMarkup]:
    """Message when free user hits conversation limit"""
    
    msg = (
        "💬 *Conversation Limit Reached*\n\n"
        "Free users get shorter conversations.\n\n"
        "*Upgrade for:*\n"
        "✅ Longer conversations\n"
        "✅ Better memory\n"
        "✅ NSFW mode\n"
        "✅ AI images\n\n"
        "🎁 Try FREE for 3 days\\!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎁 Start FREE Trial", callback_data="start_trial")],
        [InlineKeyboardButton("💎 See Plans", callback_data="show_plans")],
        [InlineKeyboardButton("« Back", callback_data="menu_main")]
    ]
    
    return msg, InlineKeyboardMarkup(keyboard)


# ============================================================================
# STRATEGIC UPSELL TRIGGERS
# ============================================================================

def should_show_trial_offer(user_id: int, message_count: int) -> bool:
    """
    Determine if we should show trial offer.
    Show after 3-5 messages for new users.
    """
    from src.payment.upsell import get_user_plan, get_trial_status
    
    # Don't show if already subscribed
    if get_user_plan(user_id):
        return False
    
    # Don't show if already had trial
    if get_trial_status(user_id):
        return False
    
    # Show after 3-5 messages
    return message_count in [3, 5]


def should_show_upgrade_reminder(user_id: int, message_count: int) -> bool:
    """
    Show upgrade reminder periodically to free users.
    Every 20 messages.
    """
    from src.payment.upsell import get_user_plan
    
    # Don't show if subscribed
    if get_user_plan(user_id):
        return False
    
    # Show every 20 messages
    return message_count > 0 and message_count % 20 == 0

