"""
Upsell and monetization system for Luna Noir bot.

Includes:
- Tiered premium plans (Basic, VIP, Ultimate)
- Pay-per-image credits
- Free trial system
- Strategic upsell prompts
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Pricing Configuration
PLANS = {
    "basic": {
        "name": "💜 Basic Premium",
        "price": "$9.99/month",
        "stripe_price_id": os.getenv("STRIPE_BASIC_PRICE_ID", "price_basic"),
        "features": [
            "✅ NSFW & FLIRTY modes unlocked",
            "✅ 20 AI images per month",
            "✅ Voice messages",
            "✅ Longer conversations (8 turns)",
            "✅ Priority response time"
        ],
        "limits": {
            "images_per_month": 20,
            "conversation_turns": 8,
            "voice_enabled": True
        }
    },
    "vip": {
        "name": "💎 VIP Premium",
        "price": "$19.99/month",
        "stripe_price_id": os.getenv("STRIPE_VIP_PRICE_ID", "price_vip"),
        "features": [
            "✅ Everything in Basic",
            "✅ UNLIMITED AI images",
            "✅ Custom outfit requests",
            "✅ Exclusive VIP scenes",
            "✅ Extended memory (16 turns)",
            "✅ Early access to new features"
        ],
        "limits": {
            "images_per_month": -1,  # Unlimited
            "conversation_turns": 16,
            "voice_enabled": True,
            "custom_outfits": True,
            "vip_scenes": True
        }
    },
    "ultimate": {
        "name": "👑 Ultimate",
        "price": "$49.99/month",
        "stripe_price_id": os.getenv("STRIPE_ULTIMATE_PRICE_ID", "price_ultimate"),
        "features": [
            "✅ Everything in VIP",
            "✅ UNLIMITED everything",
            "✅ Custom image prompts",
            "✅ Video messages (coming soon)",
            "✅ 1-on-1 priority support",
            "✅ Request custom features",
            "✅ Your name in credits"
        ],
        "limits": {
            "images_per_month": -1,
            "conversation_turns": 32,
            "voice_enabled": True,
            "custom_outfits": True,
            "vip_scenes": True,
            "custom_prompts": True,
            "video_messages": True
        }
    }
}

# Pay-per-image pricing
IMAGE_CREDIT_PRICES = {
    "5_pack": {"credits": 5, "price": "$2.99", "stripe_price_id": "price_5_images"},
    "20_pack": {"credits": 20, "price": "$9.99", "stripe_price_id": "price_20_images"},
    "50_pack": {"credits": 50, "price": "$19.99", "stripe_price_id": "price_50_images", "bonus": 10}
}

# Free trial configuration
FREE_TRIAL = {
    "duration_days": 3,
    "images_included": 5,
    "features": ["NSFW mode", "Voice messages", "AI images"]
}

# Database paths
SUBSCRIPTION_DB = Path("data/subscriptions.json")
CREDITS_DB = Path("data/credits.json")
TRIALS_DB = Path("data/trials.json")

def _load_json(path: Path) -> Dict:
    """Load JSON file or return empty dict"""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({}))
        return {}
    return json.loads(path.read_text())

def _save_json(path: Path, data: Dict):
    """Save JSON file atomically"""
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(path)

# ============================================================================
# SUBSCRIPTION MANAGEMENT
# ============================================================================

def get_user_plan(user_id: int) -> Optional[str]:
    """Get user's current subscription plan (basic, vip, ultimate, or None)"""
    subs = _load_json(SUBSCRIPTION_DB)
    user_key = str(user_id)
    
    if user_key not in subs:
        return None
    
    sub = subs[user_key]
    
    # Check if subscription is active
    if sub.get("status") != "active":
        return None
    
    # Check expiration
    expires = datetime.fromisoformat(sub.get("expires_at", "2000-01-01"))
    if datetime.now() > expires:
        return None
    
    return sub.get("plan")

def set_user_plan(user_id: int, plan: str, duration_days: int = 30):
    """Set user's subscription plan"""
    subs = _load_json(SUBSCRIPTION_DB)
    user_key = str(user_id)
    
    subs[user_key] = {
        "plan": plan,
        "status": "active",
        "started_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=duration_days)).isoformat(),
        "images_used_this_month": 0
    }
    
    _save_json(SUBSCRIPTION_DB, subs)
    logger.info(f"User {user_id} subscribed to {plan} plan")

def get_plan_limits(user_id: int) -> Dict[str, Any]:
    """Get user's plan limits"""
    plan = get_user_plan(user_id)
    
    if not plan:
        return {
            "images_per_month": 0,
            "conversation_turns": 2,
            "voice_enabled": False
        }
    
    return PLANS[plan]["limits"]

def can_generate_image(user_id: int) -> Tuple[bool, str]:
    """
    Check if user can generate an image.
    Returns (can_generate, reason_if_not)
    """
    plan = get_user_plan(user_id)
    
    # Check subscription
    if plan:
        limits = PLANS[plan]["limits"]
        
        # Unlimited images
        if limits["images_per_month"] == -1:
            return True, ""
        
        # Check monthly limit
        subs = _load_json(SUBSCRIPTION_DB)
        used = subs[str(user_id)].get("images_used_this_month", 0)
        
        if used < limits["images_per_month"]:
            return True, ""
        else:
            return False, f"Monthly limit reached ({limits['images_per_month']} images). Upgrade to VIP for unlimited!"
    
    # Check credits
    credits = get_image_credits(user_id)
    if credits > 0:
        return True, ""
    
    # Check free trial
    if has_trial_images(user_id):
        return True, ""
    
    return False, "No images remaining. Buy credits or subscribe!"

def use_image_generation(user_id: int) -> bool:
    """
    Use one image generation. Returns True if successful.
    Deducts from subscription, credits, or trial in that order.
    """
    plan = get_user_plan(user_id)
    
    # Deduct from subscription
    if plan:
        subs = _load_json(SUBSCRIPTION_DB)
        user_key = str(user_id)
        subs[user_key]["images_used_this_month"] = subs[user_key].get("images_used_this_month", 0) + 1
        _save_json(SUBSCRIPTION_DB, subs)
        return True
    
    # Deduct from credits
    if get_image_credits(user_id) > 0:
        use_image_credit(user_id)
        return True
    
    # Deduct from trial
    if has_trial_images(user_id):
        use_trial_image(user_id)
        return True
    
    return False

# ============================================================================
# IMAGE CREDITS
# ============================================================================

def get_image_credits(user_id: int) -> int:
    """Get user's remaining image credits"""
    credits = _load_json(CREDITS_DB)
    return credits.get(str(user_id), 0)

def add_image_credits(user_id: int, amount: int):
    """Add image credits to user"""
    credits = _load_json(CREDITS_DB)
    user_key = str(user_id)
    credits[user_key] = credits.get(user_key, 0) + amount
    _save_json(CREDITS_DB, credits)
    logger.info(f"Added {amount} credits to user {user_id}")

def use_image_credit(user_id: int) -> bool:
    """Use one image credit. Returns True if successful."""
    credits = _load_json(CREDITS_DB)
    user_key = str(user_id)
    
    if credits.get(user_key, 0) > 0:
        credits[user_key] -= 1
        _save_json(CREDITS_DB, credits)
        return True
    
    return False

# ============================================================================
# FREE TRIAL
# ============================================================================

def start_free_trial(user_id: int):
    """Start free trial for user"""
    trials = _load_json(TRIALS_DB)
    user_key = str(user_id)
    
    # Check if already had trial
    if user_key in trials:
        return False
    
    trials[user_key] = {
        "started_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=FREE_TRIAL["duration_days"])).isoformat(),
        "images_remaining": FREE_TRIAL["images_included"],
        "status": "active"
    }
    
    _save_json(TRIALS_DB, trials)
    logger.info(f"Started free trial for user {user_id}")
    return True

def has_trial_images(user_id: int) -> bool:
    """Check if user has trial images remaining"""
    trials = _load_json(TRIALS_DB)
    user_key = str(user_id)
    
    if user_key not in trials:
        return False
    
    trial = trials[user_key]
    
    # Check expiration
    expires = datetime.fromisoformat(trial.get("expires_at", "2000-01-01"))
    if datetime.now() > expires:
        return False
    
    return trial.get("images_remaining", 0) > 0

def use_trial_image(user_id: int) -> bool:
    """Use one trial image. Returns True if successful."""
    trials = _load_json(TRIALS_DB)
    user_key = str(user_id)
    
    if user_key in trials and trials[user_key].get("images_remaining", 0) > 0:
        trials[user_key]["images_remaining"] -= 1
        _save_json(TRIALS_DB, trials)
        return True
    
    return False

def get_trial_status(user_id: int) -> Optional[Dict]:
    """Get user's trial status"""
    trials = _load_json(TRIALS_DB)
    user_key = str(user_id)
    
    if user_key not in trials:
        return None
    
    return trials[user_key]

