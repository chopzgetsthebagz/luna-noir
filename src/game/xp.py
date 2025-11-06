"""
XP and Leveling System
Handles user experience points, level progression, and daily rewards.
"""

import time
import json
import os
from pathlib import Path

USERS = Path("data/users.json")
LEVEL_CAP = 50


def _load():
    """Load users database with gamification data"""
    if not USERS.exists():
        USERS.parent.mkdir(parents=True, exist_ok=True)
        USERS.write_text(json.dumps({
            "premium_users": [],
            "free_users": [],
            "modes": {},
            "voice": {},
            "tiers": {},
            "xp": {},
            "bond": {}
        }, indent=2))
    try:
        return json.loads(USERS.read_text())
    except Exception:
        USERS.write_text(json.dumps({
            "premium_users": [],
            "free_users": [],
            "modes": {},
            "voice": {},
            "tiers": {},
            "xp": {},
            "bond": {}
        }, indent=2))
        return json.loads(USERS.read_text())


def _save(d):
    """Save users database"""
    USERS.write_text(json.dumps(d, indent=2))


def _ensure(uid, d):
    """Ensure user has XP profile"""
    u = str(uid)
    d.setdefault("xp", {})
    d["xp"].setdefault(u, {"xp": 0, "level": 1, "last_daily": 0, "last_msg_xp": 0})


def xp_for_next(level: int) -> int:
    """Calculate XP needed for next level"""
    return 100 * level


def get_profile(uid: int):
    """
    Get user's XP profile
    
    Args:
        uid: User ID
        
    Returns:
        dict: {"xp": int, "level": int, "need": int}
    """
    d = _load()
    _ensure(uid, d)
    p = d["xp"][str(uid)]
    need = xp_for_next(p["level"])
    return {"xp": p["xp"], "level": p["level"], "need": need}


def gain_xp(uid: int, amount: int, cooldown_sec: int = 30):
    """
    Award XP to user with cooldown and auto-leveling
    
    Args:
        uid: User ID
        amount: XP amount to award
        cooldown_sec: Cooldown between XP gains (default: 30s)
        
    Returns:
        dict: Updated profile {"xp": int, "level": int, "need": int}
    """
    now = int(time.time())
    d = _load()
    _ensure(uid, d)
    p = d["xp"][str(uid)]
    
    # Per-message cooldown
    if p["last_msg_xp"] and now - p["last_msg_xp"] < cooldown_sec:
        return get_profile(uid)
    
    p["xp"] += max(0, amount)
    p["last_msg_xp"] = now
    
    # Auto level up
    while p["level"] < LEVEL_CAP and p["xp"] >= xp_for_next(p["level"]):
        p["xp"] -= xp_for_next(p["level"])
        p["level"] += 1
    
    _save(d)
    return {"xp": p["xp"], "level": p["level"], "need": xp_for_next(p["level"])}


def claim_daily(uid: int, reward: int = 20, cooldown_hours: int = 24):
    """
    Claim daily XP reward
    
    Args:
        uid: User ID
        reward: XP reward amount (default: 20)
        cooldown_hours: Hours between claims (default: 24)
        
    Returns:
        dict or None: Updated profile if successful, None if on cooldown
    """
    now = int(time.time())
    d = _load()
    _ensure(uid, d)
    p = d["xp"][str(uid)]
    
    if p["last_daily"] and now - p["last_daily"] < cooldown_hours * 3600:
        return None  # Not ready
    
    p["last_daily"] = now
    p["xp"] += reward
    
    # Level-up check
    while p["level"] < LEVEL_CAP and p["xp"] >= xp_for_next(p["level"]):
        p["xp"] -= xp_for_next(p["level"])
        p["level"] += 1
    
    _save(d)
    return {"xp": p["xp"], "level": p["level"]}

