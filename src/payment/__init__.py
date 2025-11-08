"""Payment and monetization module for Luna Noir bot."""

from .upsell import (
    get_user_plan,
    set_user_plan,
    get_plan_limits,
    can_generate_image,
    use_image_generation,
    get_image_credits,
    add_image_credits,
    start_free_trial,
    has_trial_images,
    get_trial_status,
    PLANS,
    IMAGE_CREDIT_PRICES,
    FREE_TRIAL
)

from .upsell_prompts import (
    get_image_limit_reached_message,
    get_free_trial_offer_message,
    get_nsfw_mode_upsell_message,
    get_voice_upsell_message,
    get_plans_comparison_message,
    get_credits_shop_message,
    get_trial_ending_soon_message,
    get_after_image_upsell_message,
    get_conversation_limit_message,
    should_show_trial_offer,
    should_show_upgrade_reminder
)

__all__ = [
    # Subscription management
    "get_user_plan",
    "set_user_plan",
    "get_plan_limits",
    "can_generate_image",
    "use_image_generation",
    
    # Credits
    "get_image_credits",
    "add_image_credits",
    
    # Free trial
    "start_free_trial",
    "has_trial_images",
    "get_trial_status",
    
    # Constants
    "PLANS",
    "IMAGE_CREDIT_PRICES",
    "FREE_TRIAL",
    
    # Upsell messages
    "get_image_limit_reached_message",
    "get_free_trial_offer_message",
    "get_nsfw_mode_upsell_message",
    "get_voice_upsell_message",
    "get_plans_comparison_message",
    "get_credits_shop_message",
    "get_trial_ending_soon_message",
    "get_after_image_upsell_message",
    "get_conversation_limit_message",
    "should_show_trial_offer",
    "should_show_upgrade_reminder"
]

