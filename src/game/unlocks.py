"""
Feature Unlock Gates
Controls access to features based on level or premium status.
"""

import json
from pathlib import Path

USERS = Path("data/users.json")


def _load():
    """Load users database"""
    if not USERS.exists():
        return {"premium_users": [], "tiers": {}, "xp": {}}
    return json.loads(USERS.read_text())


def is_premium(uid: int) -> bool:
    """
    Check if user has premium access (via subscription or tier)
    
    Args:
        uid: User ID
        
    Returns:
        bool: True if user has premium access
    """
    d = _load()
    return str(uid) in set(map(str, d.get("premium_users", []))) or d.get("tiers", {}).get(str(uid))


def get_level(uid: int) -> int:
    """
    Get user's current level
    
    Args:
        uid: User ID
        
    Returns:
        int: User's level (default: 1)
    """
    d = _load()
    p = d.get("xp", {}).get(str(uid), {"level": 1})
    return int(p.get("level", 1))


def get_tier(uid: int) -> str:
    """
    Get user's subscription tier
    
    Args:
        uid: User ID
        
    Returns:
        str: Tier name (BRONZE, SILVER, GOLD) or empty string
    """
    d = _load()
    return d.get("tiers", {}).get(str(uid), "")


def has_unlock(uid: int, feature: str) -> bool:
    """
    Check if user has unlocked a feature
    
    Args:
        uid: User ID
        feature: Feature name (voice, images, romantic)
        
    Returns:
        bool: True if feature is unlocked
    """
    # Default gates
    gates = {
        "voice": 2,
        "images": 3,
        "romantic": 5
    }
    
    lvl_req = gates.get(feature, 1)
    return is_premium(uid) or get_level(uid) >= lvl_req


def get_unlock_requirement(feature: str) -> int:
    """
    Get level requirement for a feature
    
    Args:
        feature: Feature name
        
    Returns:
        int: Required level
    """
    gates = {
        "voice": 2,
        "images": 3,
        "romantic": 5
    }
    return gates.get(feature, 1)

