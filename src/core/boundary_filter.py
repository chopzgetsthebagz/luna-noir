#!/usr/bin/env python3
"""
Boundary Filter for LLM Responses
Sanitizes responses to enforce safety boundaries and content policies
"""
import os
import re
import logging

logger = logging.getLogger(__name__)

MODE = os.getenv("SAFETY_MODE", "medium").lower()


def sanitize(text: str) -> str:
    """
    Basic boundary filter for tone & banned content.
    
    Modes:
    - off: No filtering (passthrough)
    - medium: Filter illegal/harmful content, light profanity control
    - strict: Aggressive filtering of adult/NSFW content
    
    Args:
        text: Raw LLM response
    
    Returns:
        Sanitized text safe for Telegram
    """
    if MODE == "off":
        logger.debug("Safety filter disabled (MODE=off)")
        return text[:4000]  # Telegram message limit
    
    clean = text
    
    # CRITICAL: Filter illegal/harmful content (all modes)
    banned_patterns = [
        r"(?i)\b(child|underage|minor|kid|teen|adolescent).*?(sex|sexual|nude|porn)",
        r"(?i)\b(rape|rapist|molest|assault)\b",
        r"(?i)\b(kill|murder|suicide|self-harm).*?(how|guide|instructions)",
        r"(?i)\b(bomb|explosive|weapon).*?(make|build|create)",
        r"(?i)\b(drug|meth|heroin).*?(cook|manufacture|synthesize)",
    ]
    
    for pattern in banned_patterns:
        if re.search(pattern, clean):
            logger.warning(f"Blocked harmful content matching: {pattern}")
            clean = re.sub(pattern, "[CONTENT FILTERED]", clean)
    
    # MEDIUM MODE: Light content control
    if MODE == "medium":
        # Replace excessive profanity
        profanity = [
            (r"\bf\*\*\*", "[censored]"),
            (r"\bf\*ck", "[censored]"),
            (r"\bsh\*t", "[censored]"),
        ]
        for pattern, replacement in profanity:
            clean = re.sub(pattern, replacement, clean, flags=re.IGNORECASE)
    
    # STRICT MODE: Aggressive NSFW filtering
    if MODE == "strict":
        nsfw_patterns = [
            (r"(?i)\b(sex|sexual|fuck|fucking)\b", "[restricted]"),
            (r"(?i)\b(nude|naked|porn|nsfw)\b", "[restricted]"),
            (r"(?i)\b(dick|cock|pussy|cunt|tits|ass)\b", "[restricted]"),
            (r"(?i)\b(orgasm|cum|ejaculate)\b", "[restricted]"),
        ]
        
        for pattern, replacement in nsfw_patterns:
            clean = re.sub(pattern, replacement, clean)
    
    # Remove excessive newlines
    clean = re.sub(r"\n{4,}", "\n\n\n", clean)
    
    # Truncate to Telegram limit (4096 chars)
    if len(clean) > 4000:
        logger.warning(f"Response truncated from {len(clean)} to 4000 chars")
        clean = clean[:3997] + "..."
    
    # Log filtering stats
    if clean != text:
        logger.info(f"Filtered response: {len(text)} -> {len(clean)} chars")
    
    return clean


def check_boundaries(text: str) -> tuple[bool, str]:
    """
    Check if text violates boundaries without modifying it.
    
    Returns:
        (is_safe, reason) - True if safe, False with reason if blocked
    """
    # Critical violations that should block the entire response
    critical_patterns = [
        (r"(?i)\b(child|underage|minor).*?(sex|sexual|nude)", "illegal content"),
        (r"(?i)\b(rape|molest)\b", "violence/assault"),
        (r"(?i)\b(kill|murder).*?(how|guide)", "harmful instructions"),
    ]
    
    for pattern, reason in critical_patterns:
        if re.search(pattern, text):
            logger.error(f"BLOCKED: {reason} - pattern: {pattern}")
            return False, reason
    
    return True, ""


def get_safety_info() -> dict:
    """Get current safety filter configuration"""
    return {
        "mode": MODE,
        "enabled": MODE != "off",
        "level": "strict" if MODE == "strict" else "medium" if MODE == "medium" else "disabled"
    }

