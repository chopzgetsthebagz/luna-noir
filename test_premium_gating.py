#!/usr/bin/env python3
"""
Test script for premium gating of FLIRTY/NSFW modes
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.bot import (
    get_user_mode, set_user_mode, is_premium,
    build_mode_keyboard, get_mode_system_prompt,
    MODE_SAFE, MODE_FLIRTY, MODE_NSFW,
    _load_db, _save_db
)

print("=" * 70)
print("TESTING PREMIUM GATING FOR FLIRTY/NSFW MODES")
print("=" * 70)

# Test 1: Database schema
print("\n✓ Test 1: Database schema includes modes")
db = _load_db()
assert "premium_users" in db, "Missing premium_users"
assert "free_users" in db, "Missing free_users"
assert "modes" in db, "Missing modes"
print(f"  Database keys: {list(db.keys())}")
print("  ✅ PASS")

# Test 2: Free user defaults to SAFE mode
print("\n✓ Test 2: Free user defaults to SAFE mode")
free_user_id = 999001
mode = get_user_mode(free_user_id)
assert mode == MODE_SAFE, f"Expected {MODE_SAFE}, got {mode}"
print(f"  Free user {free_user_id} mode: {mode}")
print("  ✅ PASS")

# Test 3: Free user can set SAFE mode
print("\n✓ Test 3: Free user can set SAFE mode")
set_user_mode(free_user_id, MODE_SAFE)
mode = get_user_mode(free_user_id)
assert mode == MODE_SAFE, f"Expected {MODE_SAFE}, got {mode}"
print(f"  Free user {free_user_id} mode after setting SAFE: {mode}")
print("  ✅ PASS")

# Test 4: Free user can attempt to set FLIRTY (but will be blocked in handler)
print("\n✓ Test 4: Free user can set FLIRTY in DB (gating happens in handler)")
set_user_mode(free_user_id, MODE_FLIRTY)
mode = get_user_mode(free_user_id)
assert mode == MODE_FLIRTY, f"Expected {MODE_FLIRTY}, got {mode}"
print(f"  Free user {free_user_id} mode in DB: {mode}")
print("  Note: Handler will block actual usage")
print("  ✅ PASS")

# Test 5: Premium user check
print("\n✓ Test 5: Premium user check")
premium_user_id = 1633265688  # From data/users.json
is_prem = is_premium(premium_user_id)
assert is_prem, f"User {premium_user_id} should be premium"
print(f"  User {premium_user_id} premium status: {is_prem}")
print("  ✅ PASS")

# Test 6: Premium user can use all modes
print("\n✓ Test 6: Premium user can use all modes")
for mode in [MODE_SAFE, MODE_FLIRTY, MODE_NSFW]:
    set_user_mode(premium_user_id, mode)
    retrieved_mode = get_user_mode(premium_user_id)
    assert retrieved_mode == mode, f"Expected {mode}, got {retrieved_mode}"
    print(f"  Premium user {premium_user_id} set to {mode}: ✓")
print("  ✅ PASS")

# Test 7: Keyboard for free user shows locked modes
print("\n✓ Test 7: Keyboard for free user shows locked modes")
set_user_mode(free_user_id, MODE_SAFE)
keyboard = build_mode_keyboard(MODE_SAFE, free_user_id)
print(f"  Keyboard type: {type(keyboard).__name__}")
print(f"  Rows: {len(keyboard.inline_keyboard)}")
# First row: mode buttons
assert len(keyboard.inline_keyboard) >= 1, "Expected at least 1 row"
first_row = keyboard.inline_keyboard[0]
print(f"  First row buttons: {len(first_row)}")
assert len(first_row) == 3, f"Expected 3 mode buttons, got {len(first_row)}"
# Check for locked buttons
locked_count = sum(1 for btn in first_row if "locked" in btn.callback_data)
print(f"  Locked buttons: {locked_count}")
assert locked_count == 2, f"Expected 2 locked buttons (FLIRTY, NSFW), got {locked_count}"
# Second row: upgrade button
assert len(keyboard.inline_keyboard) == 2, "Expected 2 rows (modes + upgrade)"
upgrade_row = keyboard.inline_keyboard[1]
assert len(upgrade_row) == 1, "Expected 1 upgrade button"
assert "upgrade" in upgrade_row[0].callback_data, "Expected upgrade callback"
print("  ✅ PASS")

# Test 8: Keyboard for premium user shows all unlocked
print("\n✓ Test 8: Keyboard for premium user shows all unlocked")
keyboard = build_mode_keyboard(MODE_NSFW, premium_user_id)
print(f"  Rows: {len(keyboard.inline_keyboard)}")
assert len(keyboard.inline_keyboard) == 1, "Expected 1 row (no upgrade button)"
first_row = keyboard.inline_keyboard[0]
assert len(first_row) == 3, f"Expected 3 mode buttons, got {len(first_row)}"
locked_count = sum(1 for btn in first_row if "locked" in btn.callback_data)
print(f"  Locked buttons: {locked_count}")
assert locked_count == 0, f"Expected 0 locked buttons for premium, got {locked_count}"
print("  ✅ PASS")

# Test 9: System prompts include length constraint for free users
print("\n✓ Test 9: System prompts include length constraint for free users")
free_prompt = get_mode_system_prompt(MODE_SAFE, is_premium_user=False)
premium_prompt = get_mode_system_prompt(MODE_SAFE, is_premium_user=True)
print(f"  Free prompt length: {len(free_prompt)}")
print(f"  Premium prompt length: {len(premium_prompt)}")
assert "60 tokens" in free_prompt or "1-2 sentences" in free_prompt, "Free prompt should mention length limit"
assert "60 tokens" not in premium_prompt and "1-2 sentences" not in premium_prompt, "Premium prompt should not mention length limit"
print("  ✅ PASS")

# Test 10: All mode prompts work
print("\n✓ Test 10: All mode prompts work")
for mode in [MODE_SAFE, MODE_FLIRTY, MODE_NSFW]:
    for is_prem in [True, False]:
        prompt = get_mode_system_prompt(mode, is_prem)
        assert len(prompt) > 0, f"Empty prompt for {mode}, premium={is_prem}"
        print(f"  {mode} (premium={is_prem}): {prompt[:50]}...")
print("  ✅ PASS")

# Test 11: Mode persistence in users.json
print("\n✓ Test 11: Mode persistence in users.json")
test_user = 888888
set_user_mode(test_user, MODE_FLIRTY)
db = _load_db()
assert str(test_user) in db["modes"], f"User {test_user} not in modes"
assert db["modes"][str(test_user)] == MODE_FLIRTY, f"Expected FLIRTY, got {db['modes'][str(test_user)]}"
print(f"  User {test_user} mode in DB: {db['modes'][str(test_user)]}")
print("  ✅ PASS")

# Test 12: Verify data/users.json structure
print("\n✓ Test 12: Verify data/users.json structure")
users_path = Path("data/users.json")
assert users_path.exists(), "data/users.json does not exist"
with open(users_path) as f:
    data = json.load(f)
print(f"  Premium users: {len(data.get('premium_users', []))}")
print(f"  Free users: {len(data.get('free_users', []))}")
print(f"  Modes stored: {len(data.get('modes', {}))}")
print("  ✅ PASS")

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED!")
print("=" * 70)

print("\n📋 SUMMARY:")
print("  ✅ Database schema updated with modes")
print("  ✅ Free users default to SAFE mode")
print("  ✅ Premium users can use all modes")
print("  ✅ Keyboard shows locked modes for free users")
print("  ✅ Keyboard shows upgrade button for free users")
print("  ✅ System prompts include length limits for free users")
print("  ✅ Mode persistence works in users.json")

print("\n🧪 MANUAL TEST STEPS:")
print("  1. Start bot: python src/server/app.py")
print("  2. As FREE user:")
print("     - Send /start → See SAFE mode, locked FLIRTY/NSFW, upgrade button")
print("     - Send /status → See 'Free Tier'")
print("     - Try to switch to FLIRTY → See 'Premium only' alert")
print("     - Send message in SAFE mode → Get short reply")
print("     - Send /upgrade → Get Stripe checkout URL")
print("  3. As PREMIUM user (simulate by adding to premium_users):")
print("     - Send /start → See all modes unlocked, no upgrade button")
print("     - Send /status → See 'Premium Active'")
print("     - Switch to FLIRTY → Works")
print("     - Switch to NSFW → Works")
print("     - Send message → Get full-length reply")

print("\n✅ Ready to test!")

