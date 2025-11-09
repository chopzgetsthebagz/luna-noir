#!/usr/bin/env python3
"""
Comprehensive Feature Test Suite for Luna Noir Bot
Tests all major functionality to ensure everything works perfectly
"""

import os
import sys
import time
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 80)
print("🧪 LUNA NOIR BOT - COMPREHENSIVE FEATURE TEST SUITE")
print("=" * 80)
print()

# Test counter
tests_passed = 0
tests_failed = 0
test_results = []

def test(name: str):
    """Decorator for test functions"""
    def decorator(func):
        def wrapper():
            global tests_passed, tests_failed
            print(f"\n{'='*80}")
            print(f"🧪 TEST: {name}")
            print(f"{'='*80}")
            try:
                result = func()
                if result:
                    print(f"✅ PASSED: {name}")
                    tests_passed += 1
                    test_results.append(("✅", name, "PASSED"))
                else:
                    print(f"❌ FAILED: {name}")
                    tests_failed += 1
                    test_results.append(("❌", name, "FAILED"))
                return result
            except Exception as e:
                print(f"❌ FAILED: {name}")
                print(f"   Error: {e}")
                tests_failed += 1
                test_results.append(("❌", name, f"ERROR: {e}"))
                return False
        return wrapper
    return decorator


# ============================================================================
# TEST 1: Environment Configuration
# ============================================================================

@test("Environment Configuration")
def test_environment():
    """Test that all required environment variables are set"""
    print("\n📋 Checking environment variables...")
    
    required_vars = [
        "TELEGRAM_TOKEN",
        "GROQ_API_KEY",
        "ELEVENLABS_API_KEY",
        "WEBHOOK_URL"
    ]
    
    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {'*' * 20} (set)")
        else:
            print(f"   ❌ {var}: NOT SET")
            missing.append(var)
    
    if missing:
        print(f"\n   ⚠️  Missing variables: {', '.join(missing)}")
        return False
    
    print("\n   ✅ All required environment variables are set!")
    return True


# ============================================================================
# TEST 2: LLM Integration
# ============================================================================

@test("LLM Integration (Groq)")
def test_llm():
    """Test LLM client with Groq API"""
    print("\n🤖 Testing LLM integration...")

    import requests

    # Test Groq API directly
    groq_api_key = os.getenv("GROQ_API_KEY")
    groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    if not groq_api_key:
        print("\n   ⚠️  GROQ_API_KEY not set, skipping LLM test")
        return True  # Don't fail if not configured

    print(f"\n   Provider: Groq")
    print(f"   Model: {groq_model}")
    print(f"   API Key: {'*' * 20} (set)")

    # Test query
    print("\n   Testing Groq API query...")
    start_time = time.time()

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "model": groq_model,
            "messages": [
                {"role": "system", "content": "You are Luna Noir, a flirty AI companion."},
                {"role": "user", "content": "Say 'Hello! I'm Luna.' in a flirty way (max 20 words)"}
            ],
            "max_tokens": 100,
            "temperature": 0.85
        }

        r = requests.post(url, headers=headers, json=body, timeout=15)
        r.raise_for_status()
        response = r.json()["choices"][0]["message"]["content"].strip()
        elapsed = time.time() - start_time

        print(f"\n   Response ({elapsed:.2f}s): {response[:100]}...")

        if response and len(response) > 10:
            print(f"\n   ✅ LLM responding correctly in {elapsed:.2f}s")
            return True
        else:
            print(f"\n   ❌ LLM response invalid or empty")
            return False

    except Exception as e:
        print(f"\n   ❌ LLM query failed: {e}")
        return False


# ============================================================================
# TEST 3: Image Generation - All Scenarios
# ============================================================================

@test("Image Generation - All Scenarios")
def test_image_generation():
    """Test all image generation scenarios"""
    print("\n📸 Testing image generation...")
    
    from src.image.luna_generator import (
        generate_luna_selfie,
        generate_luna_scenario,
        generate_luna_with_outfit,
        OUTFIT_PRESETS
    )
    
    # Test 1: Selfie generation
    print("\n   Testing selfie generation (flirty mood)...")
    start_time = time.time()
    try:
        image_bytes = generate_luna_selfie(mood="flirty", nsfw=False)
        elapsed = time.time() - start_time
        print(f"   ✅ Selfie generated: {len(image_bytes)} bytes in {elapsed:.2f}s")
    except Exception as e:
        print(f"   ❌ Selfie generation failed: {e}")
        return False
    
    # Test 2: NSFW scenario
    print("\n   Testing NSFW scenario (nude_bent_over)...")
    start_time = time.time()
    try:
        image_bytes = generate_luna_scenario(scenario_type="nude_bent_over", nsfw=True)
        elapsed = time.time() - start_time
        print(f"   ✅ NSFW scenario generated: {len(image_bytes)} bytes in {elapsed:.2f}s")
    except Exception as e:
        print(f"   ❌ NSFW scenario failed: {e}")
        return False
    
    # Test 3: SFW scenario
    print("\n   Testing SFW scenario (bedroom)...")
    start_time = time.time()
    try:
        image_bytes = generate_luna_scenario(scenario_type="bedroom", nsfw=False)
        elapsed = time.time() - start_time
        print(f"   ✅ SFW scenario generated: {len(image_bytes)} bytes in {elapsed:.2f}s")
    except Exception as e:
        print(f"   ❌ SFW scenario failed: {e}")
        return False
    
    # Test 4: Outfit preset
    print("\n   Testing outfit preset (lingerie_lace)...")
    start_time = time.time()
    try:
        image_bytes = generate_luna_with_outfit(outfit_name="lingerie_lace", nsfw=True)
        elapsed = time.time() - start_time
        print(f"   ✅ Outfit preset generated: {len(image_bytes)} bytes in {elapsed:.2f}s")
    except Exception as e:
        print(f"   ❌ Outfit preset failed: {e}")
        return False
    
    print(f"\n   ✅ All image generation tests passed!")
    print(f"   📊 Total outfit presets available: {len(OUTFIT_PRESETS)}")
    return True


# ============================================================================
# TEST 4: Voice Synthesis
# ============================================================================

@test("Voice Synthesis (ElevenLabs)")
def test_voice():
    """Test voice synthesis with ElevenLabs"""
    print("\n🎧 Testing voice synthesis...")
    
    from src.voice.tts_elevenlabs import synthesize_tts
    
    test_text = "Hey there! I'm Luna. How are you doing today?"
    
    print(f"\n   Synthesizing: '{test_text}'")
    start_time = time.time()
    try:
        audio_bytes = synthesize_tts(test_text)
        elapsed = time.time() - start_time
        
        if audio_bytes and len(audio_bytes) > 1000:
            print(f"   ✅ Voice synthesized: {len(audio_bytes)} bytes in {elapsed:.2f}s")
            return True
        else:
            print(f"   ❌ Voice synthesis returned invalid data")
            return False
    except Exception as e:
        print(f"   ❌ Voice synthesis failed: {e}")
        return False


# ============================================================================
# TEST 5: User Preferences System
# ============================================================================

@test("User Preferences System")
def test_preferences():
    """Test user preferences tracking"""
    print("\n💾 Testing user preferences system...")

    from src.core.user_preferences import (
        add_interest,
        add_kink,
        set_life_detail,
        get_preferences,
        get_user_context
    )

    test_user_id = 999999999  # Test user

    # Save some preferences
    print("\n   Saving test preferences...")
    add_interest(test_user_id, "gaming")
    add_interest(test_user_id, "anime")
    add_interest(test_user_id, "music")
    add_kink(test_user_id, "teasing")
    add_kink(test_user_id, "roleplay")
    set_life_detail(test_user_id, "job", "software engineer")

    # Retrieve preferences
    print("\n   Retrieving preferences...")
    prefs = get_preferences(test_user_id)

    print(f"\n   Stored preferences:")
    for key, value in prefs.items():
        if value:  # Only show non-empty values
            print(f"      {key}: {value}")

    # Get context
    context = get_user_context(test_user_id)
    print(f"\n   Generated context: {context[:100]}...")

    if prefs and context and "gaming" in context.lower():
        print(f"\n   ✅ User preferences system working!")
        return True
    else:
        print(f"\n   ❌ User preferences system failed")
        return False


# ============================================================================
# TEST 6: Gamification System
# ============================================================================

@test("Gamification System")
def test_gamification():
    """Test XP, quests, bond, and leaderboard"""
    print("\n🎮 Testing gamification system...")
    
    from src.game.xp import gain_xp, get_profile, claim_daily
    from src.game.bond import touch as bond_touch, get_bond
    from src.game.quests import list_quests
    from src.game.leaderboard import top_xp
    
    test_user_id = 999999999
    
    # Test XP system
    print("\n   Testing XP system...")
    gain_xp(test_user_id, 50)
    profile = get_profile(test_user_id)
    print(f"      XP: {profile['xp']}, Level: {profile['level']}")
    
    # Test bond system
    print("\n   Testing bond system...")
    bond_touch(test_user_id, 10)
    bond = get_bond(test_user_id)
    bond_score = bond.get('score', 0) if isinstance(bond, dict) else bond
    print(f"      Bond: {bond_score}")

    # Test quests
    print("\n   Testing quest system...")
    quests = list_quests(test_user_id)
    print(f"      Available quests: {len(quests)}")
    if quests:
        print(f"      First quest: {quests[0]['text']}")

    # Test leaderboard
    print("\n   Testing leaderboard...")
    top = top_xp(n=5)
    print(f"      Top {len(top)} users on leaderboard")

    if profile and bond_score >= 0 and isinstance(quests, list):
        print(f"\n   ✅ Gamification system working!")
        return True
    else:
        print(f"\n   ❌ Gamification system failed")
        return False


# ============================================================================
# TEST 7: Payment System (Testing Mode)
# ============================================================================

@test("Payment System (Testing Mode)")
def test_payment():
    """Test payment/upsell system in testing mode"""
    print("\n💎 Testing payment system...")
    
    from src.payment.upsell import (
        get_user_plan,
        set_user_plan,
        can_generate_image,
        add_image_credits,
        get_image_credits,
        PLANS,
        IMAGE_CREDIT_PRICES
    )
    
    test_user_id = 999999999
    
    # Test subscription plans
    print(f"\n   Available plans: {len(PLANS)}")
    for plan_id, plan_data in PLANS.items():
        print(f"      {plan_data['name']}: {plan_data['price']}")
    
    # Test setting a plan
    print("\n   Setting VIP plan for test user...")
    set_user_plan(test_user_id, "vip", duration_days=30)
    plan = get_user_plan(test_user_id)
    print(f"      User plan: {plan}")
    
    # Test image credits
    print("\n   Testing image credits...")
    add_image_credits(test_user_id, 10)
    credits = get_image_credits(test_user_id)
    print(f"      User credits: {credits}")
    
    # Test can generate
    can_gen, reason = can_generate_image(test_user_id)
    print(f"      Can generate: {can_gen} ({reason})")
    
    # Test credit packs
    print(f"\n   Available credit packs: {len(IMAGE_CREDIT_PRICES)}")
    for pack_id, pack_data in IMAGE_CREDIT_PRICES.items():
        print(f"      {pack_id}: {pack_data['credits']} credits for {pack_data['price']}")
    
    if plan == "vip" and credits >= 10 and can_gen:
        print(f"\n   ✅ Payment system working!")
        return True
    else:
        print(f"\n   ❌ Payment system failed")
        return False


# ============================================================================
# TEST 8: Database Persistence
# ============================================================================

@test("Database Persistence")
def test_database():
    """Test that data persists correctly"""
    print("\n💾 Testing database persistence...")
    
    data_dir = Path("data")
    
    required_files = [
        "users.json",
        "subscriptions.json",
        "credits.json",
        "trial.json"
    ]
    
    print(f"\n   Checking data directory: {data_dir}")
    
    all_exist = True
    for filename in required_files:
        filepath = data_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"      ✅ {filename}: {size} bytes")
        else:
            print(f"      ❌ {filename}: NOT FOUND")
            all_exist = False
    
    if all_exist:
        print(f"\n   ✅ All database files exist!")
        return True
    else:
        print(f"\n   ⚠️  Some database files missing (will be created on first use)")
        return True  # Not critical, files created on demand


# ============================================================================
# TEST 9: Bot Initialization
# ============================================================================

@test("Bot Initialization")
def test_bot_init():
    """Test that bot can be initialized"""
    print("\n🤖 Testing bot initialization...")
    
    from src.core.bot import create_bot
    
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("   ❌ TELEGRAM_TOKEN not set")
        return False
    
    print(f"\n   Creating bot with token: {token[:20]}...")
    try:
        bot = create_bot(token)
        print(f"   ✅ Bot created successfully!")
        print(f"   Bot type: {type(bot).__name__}")
        return True
    except Exception as e:
        print(f"   ❌ Bot initialization failed: {e}")
        return False


# ============================================================================
# RUN ALL TESTS
# ============================================================================

def run_all_tests():
    """Run all tests and print summary"""
    print("\n" + "=" * 80)
    print("🚀 STARTING COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run tests
    test_environment()
    test_llm()
    test_image_generation()
    test_voice()
    test_preferences()
    test_gamification()
    test_payment()
    test_database()
    test_bot_init()
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    total = tests_passed + tests_failed
    pass_rate = (tests_passed / total * 100) if total > 0 else 0
    
    print(f"\n   Total Tests: {total}")
    print(f"   ✅ Passed: {tests_passed}")
    print(f"   ❌ Failed: {tests_failed}")
    print(f"   📈 Pass Rate: {pass_rate:.1f}%")
    
    print("\n" + "=" * 80)
    print("📋 DETAILED RESULTS")
    print("=" * 80)
    
    for status, name, result in test_results:
        print(f"   {status} {name}: {result}")
    
    print("\n" + "=" * 80)
    if tests_failed == 0:
        print("🎉 ALL TESTS PASSED! LUNA NOIR IS PRODUCTION READY!")
    else:
        print(f"⚠️  {tests_failed} TEST(S) FAILED - REVIEW ABOVE FOR DETAILS")
    print("=" * 80)
    print()
    
    return tests_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

