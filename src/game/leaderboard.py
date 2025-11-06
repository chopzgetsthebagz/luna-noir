"""
Leaderboard System
Rankings based on XP and levels.
"""

import json
from pathlib import Path

USERS = Path("data/users.json")


def top_xp(n=10):
    """
    Get top users by XP and level
    
    Args:
        n: Number of top users to return (default: 10)
        
    Returns:
        list: Tuples of (uid, level, xp) sorted by level and XP
    """
    if not USERS.exists():
        return []
    
    d = json.loads(USERS.read_text())
    xp = d.get("xp", {})
    items = []
    
    for uid, p in xp.items():
        items.append((uid, int(p.get("level", 1)), int(p.get("xp", 0))))
    
    items.sort(key=lambda t: (t[1], t[2]), reverse=True)
    return items[:n]


def mask_uid(uid: str) -> str:
    """
    Mask user ID for privacy (show first 3 and last 2 digits)
    
    Args:
        uid: User ID string
        
    Returns:
        str: Masked UID
    """
    if len(uid) <= 5:
        return uid
    return f"{uid[:3]}...{uid[-2:]}"

