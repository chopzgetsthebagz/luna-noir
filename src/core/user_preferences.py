"""
User Preferences System
Tracks user interests, kinks, life details for personalized responses
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

PREFS_DIR = Path("data/preferences")
PREFS_DIR.mkdir(parents=True, exist_ok=True)


def _get_pref_file(user_id: int) -> Path:
    """Get preference file path for user"""
    return PREFS_DIR / f"{user_id}.json"


def _load_prefs(user_id: int) -> Dict[str, Any]:
    """Load user preferences"""
    pref_file = _get_pref_file(user_id)
    if not pref_file.exists():
        return {
            "interests": [],  # General interests (gaming, music, etc.)
            "kinks": [],  # Sexual preferences/kinks
            "life_details": {},  # Job, location, relationship status, etc.
            "favorite_topics": [],  # Topics they like to discuss
            "dislikes": [],  # Things they don't like
            "personality_notes": [],  # Notes about their personality
            "conversation_style": "casual",  # casual, formal, playful, etc.
            "last_updated": None
        }
    try:
        return json.loads(pref_file.read_text())
    except Exception as e:
        logger.error(f"Error loading preferences for {user_id}: {e}")
        return {}


def _save_prefs(user_id: int, prefs: Dict[str, Any]):
    """Save user preferences"""
    pref_file = _get_pref_file(user_id)
    try:
        pref_file.write_text(json.dumps(prefs, indent=2))
    except Exception as e:
        logger.error(f"Error saving preferences for {user_id}: {e}")


def get_user_context(user_id: int) -> str:
    """
    Get formatted user context for system prompt
    
    Args:
        user_id: User ID
        
    Returns:
        Formatted string with user preferences and context
    """
    prefs = _load_prefs(user_id)
    
    context_parts = []
    
    # Interests
    if prefs.get("interests"):
        interests_str = ", ".join(prefs["interests"])
        context_parts.append(f"Their interests: {interests_str}")
    
    # Kinks/preferences
    if prefs.get("kinks"):
        kinks_str = ", ".join(prefs["kinks"])
        context_parts.append(f"Their kinks/preferences: {kinks_str}")
    
    # Life details
    life = prefs.get("life_details", {})
    if life:
        life_parts = []
        if life.get("job"):
            life_parts.append(f"works as {life['job']}")
        if life.get("location"):
            life_parts.append(f"lives in {life['location']}")
        if life.get("relationship_status"):
            life_parts.append(f"relationship status: {life['relationship_status']}")
        if life.get("age"):
            life_parts.append(f"age {life['age']}")
        if life_parts:
            context_parts.append(f"About them: {', '.join(life_parts)}")
    
    # Favorite topics
    if prefs.get("favorite_topics"):
        topics_str = ", ".join(prefs["favorite_topics"])
        context_parts.append(f"Loves talking about: {topics_str}")
    
    # Dislikes
    if prefs.get("dislikes"):
        dislikes_str = ", ".join(prefs["dislikes"])
        context_parts.append(f"Dislikes: {dislikes_str}")
    
    # Personality notes
    if prefs.get("personality_notes"):
        notes_str = "; ".join(prefs["personality_notes"][-3:])  # Last 3 notes
        context_parts.append(f"Personality: {notes_str}")
    
    if context_parts:
        return "\n".join(context_parts)
    else:
        return "No user preferences learned yet. Pay attention to what they share and remember it."


def add_interest(user_id: int, interest: str):
    """Add an interest to user profile"""
    prefs = _load_prefs(user_id)
    if "interests" not in prefs:
        prefs["interests"] = []
    if interest not in prefs["interests"]:
        prefs["interests"].append(interest)
        _save_prefs(user_id, prefs)
        logger.info(f"Added interest '{interest}' for user {user_id}")


def add_kink(user_id: int, kink: str):
    """Add a kink/preference to user profile"""
    prefs = _load_prefs(user_id)
    if "kinks" not in prefs:
        prefs["kinks"] = []
    if kink not in prefs["kinks"]:
        prefs["kinks"].append(kink)
        _save_prefs(user_id, prefs)
        logger.info(f"Added kink '{kink}' for user {user_id}")


def set_life_detail(user_id: int, key: str, value: str):
    """Set a life detail (job, location, etc.)"""
    prefs = _load_prefs(user_id)
    if "life_details" not in prefs:
        prefs["life_details"] = {}
    prefs["life_details"][key] = value
    _save_prefs(user_id, prefs)
    logger.info(f"Set {key}='{value}' for user {user_id}")


def add_personality_note(user_id: int, note: str):
    """Add a personality observation"""
    prefs = _load_prefs(user_id)
    if "personality_notes" not in prefs:
        prefs["personality_notes"] = []
    prefs["personality_notes"].append(note)
    # Keep only last 10 notes
    if len(prefs["personality_notes"]) > 10:
        prefs["personality_notes"] = prefs["personality_notes"][-10:]
    _save_prefs(user_id, prefs)
    logger.info(f"Added personality note for user {user_id}")


def get_preferences(user_id: int) -> Dict[str, Any]:
    """Get all user preferences"""
    return _load_prefs(user_id)


def clear_preferences(user_id: int):
    """Clear all user preferences"""
    pref_file = _get_pref_file(user_id)
    if pref_file.exists():
        pref_file.unlink()
        logger.info(f"Cleared preferences for user {user_id}")

