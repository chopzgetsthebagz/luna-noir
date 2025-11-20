"""
Test mode for payment system - simulates Stripe payments for testing.

This allows you to test the entire payment flow without setting up Stripe.
Users can "purchase" subscriptions and credits with test commands.
"""

import logging
from typing import Optional
from datetime import datetime, timedelta

from .upsell import (
    set_user_plan, add_image_credits, start_free_trial,
    PLANS, IMAGE_CREDIT_PRICES, _load_json, _save_json,
    SUBSCRIPTION_DB, CREDITS_DB, TRIALS_DB
)

logger = logging.getLogger(__name__)

# Test mode flag
TEST_MODE_ENABLED = True

def simulate_subscription_purchase(user_id: int, plan: str) -> bool:
    """
    Simulate a subscription purchase in test mode.
    
    Args:
        user_id: Telegram user ID
        plan: Plan name (basic, vip, ultimate)
    
    Returns:
        True if successful
    """
    if plan not in PLANS:
        logger.error(f"Invalid plan: {plan}")
        return False
    
    # Set the subscription (30 days)
    set_user_plan(user_id, plan, duration_days=30)
    
    logger.info(f"TEST MODE: User {user_id} purchased {plan} plan")
    return True

def simulate_credits_purchase(user_id: int, pack: str) -> bool:
    """
    Simulate a credits purchase in test mode.
    
    Args:
        user_id: Telegram user ID
        pack: Pack name (5_pack, 20_pack, 50_pack)
    
    Returns:
        True if successful
    """
    if pack not in IMAGE_CREDIT_PRICES:
        logger.error(f"Invalid pack: {pack}")
        return False
    
    pack_info = IMAGE_CREDIT_PRICES[pack]
    credits = pack_info["credits"]
    
    # Add bonus if applicable
    if "bonus" in pack_info:
        credits += pack_info["bonus"]
    
    add_image_credits(user_id, credits)
    
    logger.info(f"TEST MODE: User {user_id} purchased {pack} ({credits} credits)")
    return True

def simulate_free_trial(user_id: int) -> bool:
    """
    Simulate starting a free trial.
    
    Args:
        user_id: Telegram user ID
    
    Returns:
        True if successful
    """
    success = start_free_trial(user_id)
    
    if success:
        logger.info(f"TEST MODE: User {user_id} started free trial")
    else:
        logger.warning(f"TEST MODE: User {user_id} already had trial")
    
    return success

def get_test_payment_url(user_id: int, product_type: str, product_id: str) -> str:
    """
    Generate a fake payment URL for test mode.
    In real mode, this would be a Stripe checkout URL.
    
    Args:
        user_id: Telegram user ID
        product_type: 'subscription' or 'credits'
        product_id: Plan name or pack name
    
    Returns:
        Fake URL string
    """
    return f"https://test-payment.luna-noir.bot/{product_type}/{product_id}?user={user_id}"

def reset_user_payments(user_id: int):
    """
    Reset all payment data for a user (for testing).
    
    Args:
        user_id: Telegram user ID
    """
    user_key = str(user_id)
    
    # Remove subscription
    subs = _load_json(SUBSCRIPTION_DB)
    if user_key in subs:
        del subs[user_key]
        _save_json(SUBSCRIPTION_DB, subs)
    
    # Remove credits
    credits = _load_json(CREDITS_DB)
    if user_key in credits:
        del credits[user_key]
        _save_json(CREDITS_DB, credits)
    
    # Remove trial
    trials = _load_json(TRIALS_DB)
    if user_key in trials:
        del trials[user_key]
        _save_json(TRIALS_DB, trials)
    
    logger.info(f"TEST MODE: Reset all payment data for user {user_id}")

def get_test_commands_help() -> str:
    """Get help text for test mode commands."""
    return """
🧪 **TEST MODE COMMANDS**

**Subscriptions:**
• `/testbuy basic` - Get Basic Premium ($9.99/mo)
• `/testbuy vip` - Get VIP Premium ($19.99/mo)
• `/testbuy ultimate` - Get Ultimate ($49.99/mo)

**Credits:**
• `/testbuy 5pack` - Get 5 image credits ($2.99)
• `/testbuy 20pack` - Get 20 image credits ($9.99)
• `/testbuy 50pack` - Get 60 image credits ($19.99)

**Trial:**
• `/testtrial` - Start free trial (3 days, 5 images)

**Reset:**
• `/testreset` - Reset all your payment data

**Note:** This is TEST MODE. No real money is charged!
"""

