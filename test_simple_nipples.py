#!/usr/bin/env python3
"""
Test simplified nipple description - using natural language
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.image.luna_generator import generate_luna_scenario

print("=" * 80)
print("🧪 TESTING SIMPLIFIED NIPPLE DESCRIPTION")
print("=" * 80)
print("\nNEW APPROACH - SIMPLER NATURAL LANGUAGE:")
print()
print("  1. BASE DESCRIPTION:")
print("     • Changed from: 'anatomically correct small pink nipples centered on natural round areolas'")
print("     • To: 'normal human nipples'")
print("     • Reason: Let AI use its training on real human anatomy")
print()
print("  2. NSFW PROMPTS:")
print("     • Changed from: 'anatomically correct body, natural breast shape, small pink nipples...'")
print("     • To: 'realistic female anatomy, natural breasts, normal nipples'")
print("     • Reason: Simpler = more natural results")
print()
print("  3. NEGATIVE PROMPTS:")
print("     • Added: 'strange nipples, malformed nipples, distorted nipples'")
print("     • Keeps all previous blocks")
print("=" * 80)

# Test 1: Topless
print("\n1. Testing topless photo...")
try:
    image_bytes = generate_luna_scenario(scenario_type="topless", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: Standing Nude
print("\n2. Testing standing nude...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 3: Lying Nude
print("\n3. Testing lying nude...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude_lying", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 4: Bedroom
print("\n4. Testing bedroom scene...")
try:
    image_bytes = generate_luna_scenario(scenario_type="bedroom", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ SIMPLIFIED NIPPLE TEST COMPLETE")
print("=" * 80)
print("\n🔍 CHECK IF NIPPLES LOOK MORE NATURAL NOW:")
print()
print("  • Using 'normal human nipples' instead of over-describing")
print("  • Using 'realistic female anatomy' instead of technical terms")
print("  • Letting AI use its training on real human photos")
print()
print("EXPECTED RESULT:")
print("  ✓ Nipples should look like normal human nipples")
print("  ✓ Natural appearance (not weird or artificial)")
print("  ✓ Realistic proportions")
print("  ✓ No strange deformities")

