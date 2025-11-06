"""
Quest System
Daily and repeatable quests for XP rewards.
"""

import time
import json
from pathlib import Path

DB = Path("data/quests.json")

# Predefined quests
PRE = [
    {"id": "daily_greet", "text": "Say 'good morning'", "xp": 10, "key": "good morning"},
    {"id": "share_thought", "text": "Tell Luna one thing on your mind", "xp": 15, "key": "I feel"}
]


def _load():
    """Load quests database"""
    if not DB.exists():
        DB.parent.mkdir(parents=True, exist_ok=True)
        DB.write_text(json.dumps({"progress": {}, "completed": {}}, indent=2))
    return json.loads(DB.read_text())


def _save(d):
    """Save quests database"""
    DB.write_text(json.dumps(d, indent=2))


def list_quests(uid: int):
    """
    List all quests for a user
    
    Args:
        uid: User ID
        
    Returns:
        list: Quest objects with completion status
    """
    d = _load()
    done = set(d.get("completed", {}).get(str(uid), []))
    items = []
    for q in PRE:
        items.append({
            "id": q["id"],
            "text": q["text"],
            "xp": q["xp"],
            "done": q["id"] in done
        })
    return items


def try_autocomplete(uid: int, text: str):
    """
    Auto-complete quests based on message content
    
    Args:
        uid: User ID
        text: Message text
        
    Returns:
        list: Newly completed quests
    """
    d = _load()
    u = str(uid)
    done = set(d.get("completed", {}).get(u, []))
    updates = []
    
    for q in PRE:
        if q["id"] in done:
            continue
        if q["key"].lower() in (text or "").lower():
            d.setdefault("completed", {}).setdefault(u, []).append(q["id"])
            updates.append(q)
    
    if updates:
        _save(d)
    return updates


def claim(uid: int, qid: str):
    """
    Check if quest is completed
    
    Args:
        uid: User ID
        qid: Quest ID
        
    Returns:
        bool: True if quest is completed
    """
    d = _load()
    u = str(uid)
    if qid in d.get("completed", {}).get(u, []):
        return True
    return False


def get_quest_xp(qid: str) -> int:
    """
    Get XP reward for a quest
    
    Args:
        qid: Quest ID
        
    Returns:
        int: XP reward amount
    """
    for q in PRE:
        if q["id"] == qid:
            return q["xp"]
    return 0

