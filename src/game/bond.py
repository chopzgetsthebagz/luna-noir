"""
Bond Meter System
Tracks relationship strength with decay mechanics.
"""

import time
import json
from pathlib import Path

USERS = Path("data/users.json")
MAX = 100


def _load():
    """Load users database"""
    if not USERS.exists():
        return {"bond": {}}
    return json.loads(USERS.read_text())


def _save(d):
    """Save users database"""
    USERS.write_text(json.dumps(d, indent=2))


def get_bond(uid: int):
    """
    Get user's bond score
    
    Args:
        uid: User ID
        
    Returns:
        dict: {"score": int, "last_update": int}
    """
    d = _load()
    b = d.get("bond", {}).get(str(uid), {"score": 0, "last_update": 0})
    return b


def touch(uid: int, inc: int = 1, decay_after_h: int = 48, decay_amt: int = 5):
    """
    Update bond score with decay mechanics
    
    Args:
        uid: User ID
        inc: Amount to increase bond (default: 1)
        decay_after_h: Hours of inactivity before decay (default: 48)
        decay_amt: Amount to decay (default: 5)
        
    Returns:
        dict: Updated bond data
    """
    now = int(time.time())
    d = _load()
    u = str(uid)
    d.setdefault("bond", {}).setdefault(u, {"score": 0, "last_update": 0})
    b = d["bond"][u]
    
    # Decay if inactive
    if b["last_update"] and now - b["last_update"] > decay_after_h * 3600:
        b["score"] = max(0, b["score"] - decay_amt)
    
    b["score"] = min(MAX, b["score"] + inc)
    b["last_update"] = now
    
    _save(d)
    return b

