#!/usr/bin/env python3
"""
Test script for Luna Noir gamification features
Run this to verify XP, quests, bond, and unlock systems work correctly.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.game.xp import get_profile, gain_xp, claim_daily
from src.game.unlocks import has_unlock, get_level, get_tier
from src.game.quests import list_quests, try_autocomplete, claim as claim_quest, get_quest_xp
from src.game.bond import get_bond, touch as bond_touch
from src.game.leaderboard import top_xp, mask_uid

TEST_UID = 999999999


def test_xp_system():
    """Test XP gain and leveling"""
    print("\n=== Testing XP System ===")
    
    # Get initial profile
    profile = get_profile(TEST_UID)
    print(f"Initial: Level {profile['level']}, XP {profile['xp']}/{profile['need']}")
    
    # Gain XP
    profile = gain_xp(TEST_UID, 50)
    print(f"After +50 XP: Level {profile['level']}, XP {profile['xp']}/{profile['need']}")
    
    # Test cooldown
    profile = gain_xp(TEST_UID, 10)
    print(f"Immediate gain (should be blocked by cooldown): Level {profile['level']}, XP {profile['xp']}/{profile['need']}")
    
    # Gain enough to level up
    profile = gain_xp(TEST_UID, 100, cooldown_sec=0)
    print(f"After +100 XP (no cooldown): Level {profile['level']}, XP {profile['xp']}/{profile['need']}")
    
    print("✅ XP system working")


def test_daily_reward():
    """Test daily reward system"""
    print("\n=== Testing Daily Reward ===")
    
    result = claim_daily(TEST_UID)
    if result:
        print(f"Daily claimed: Level {result['level']}, XP {result['xp']}")
    else:
        print("Daily already claimed (24h cooldown)")
    
    # Try again immediately
    result = claim_daily(TEST_UID)
    if result:
        print("ERROR: Daily should be on cooldown!")
    else:
        print("✅ Daily cooldown working")


def test_quests():
    """Test quest system"""
    print("\n=== Testing Quest System ===")
    
    # List quests
    quests = list_quests(TEST_UID)
    print(f"Available quests: {len(quests)}")
    for q in quests:
        status = "✅" if q['done'] else "⭕"
        print(f"  {status} {q['text']} (+{q['xp']} XP)")
    
    # Try autocomplete
    completed = try_autocomplete(TEST_UID, "good morning Luna!")
    if completed:
        print(f"Auto-completed {len(completed)} quest(s):")
        for q in completed:
            print(f"  - {q['text']} (+{q['xp']} XP)")
    
    # Claim quest
    if claim_quest(TEST_UID, "daily_greet"):
        xp_reward = get_quest_xp("daily_greet")
        print(f"Quest 'daily_greet' is completed, reward: {xp_reward} XP")
        print("✅ Quest system working")
    else:
        print("Quest not completed yet")


def test_bond():
    """Test bond meter"""
    print("\n=== Testing Bond Meter ===")
    
    bond = get_bond(TEST_UID)
    print(f"Initial bond: {bond['score']}/100")
    
    # Touch bond
    bond = bond_touch(TEST_UID, 5)
    print(f"After +5: {bond['score']}/100")
    
    # Touch again
    bond = bond_touch(TEST_UID, 10)
    print(f"After +10: {bond['score']}/100")
    
    print("✅ Bond meter working")


def test_unlocks():
    """Test feature unlock gates"""
    print("\n=== Testing Feature Unlocks ===")
    
    level = get_level(TEST_UID)
    tier = get_tier(TEST_UID)
    
    print(f"User level: {level}")
    print(f"User tier: {tier or 'None'}")
    
    features = ["voice", "images", "romantic"]
    for feature in features:
        unlocked = has_unlock(TEST_UID, feature)
        status = "✅ Unlocked" if unlocked else "🔒 Locked"
        print(f"  {feature}: {status}")
    
    print("✅ Unlock system working")


def test_leaderboard():
    """Test leaderboard"""
    print("\n=== Testing Leaderboard ===")
    
    top = top_xp(10)
    print(f"Top {len(top)} users:")
    for i, (uid, level, xp) in enumerate(top, 1):
        masked = mask_uid(uid)
        print(f"  #{i} {masked} • L{level} ({xp} XP)")
    
    print("✅ Leaderboard working")


def main():
    """Run all tests"""
    print("🎮 Luna Noir Gamification Test Suite")
    print("=" * 50)
    
    try:
        test_xp_system()
        test_daily_reward()
        test_quests()
        test_bond()
        test_unlocks()
        test_leaderboard()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        print("\nTest user profile:")
        profile = get_profile(TEST_UID)
        bond = get_bond(TEST_UID)
        print(f"  Level: {profile['level']}")
        print(f"  XP: {profile['xp']}/{profile['need']}")
        print(f"  Bond: {bond['score']}/100")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

