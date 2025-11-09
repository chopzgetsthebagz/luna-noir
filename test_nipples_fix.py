#!/usr/bin/env python3
"""
Test improved nipple realism
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.image.luna_generator import generate_luna_scenario

print("=" * 80)
print("🧪 TESTING IMPROVED NIPPLE REALISM")
print("=" * 80)
print("\nNEW IMPROVEMENTS:")
print()
print("  1. BASE DESCRIPTION:")
print("     • Changed: 'small pink nipples and natural areolas'")
print("     • To: 'anatomically correct small pink nipples centered on natural round areolas'")
print("     • More specific about placement and shape")
print()
print("  2. NSFW PROMPTS:")
print("     • Added: 'anatomically correct female body'")
print("     • Added: 'natural breast shape with realistic nipple placement'")
print("     • Added: 'small pink nipples centered on round areolas'")
print("     • Added: 'natural human anatomy'")
print("     • Added: 'photorealistic human'")
print("     • Added: 'natural proportions'")
print()
print("  3. NEGATIVE PROMPTS:")
print("     • Added: 'weird nipples, large nipples, inverted nipples'")
print("     • Added: 'asymmetric nipples, unnatural nipples'")
print("     • Added: 'pointy nipples, cone shaped breasts'")
print("=" * 80)

# Test 1: Topless Photo
print("\n1. Testing topless photo (primary nipple test)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="topless", nsfw=True)
    print(f"   ✅ Topless photo generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Small pink nipples centered on round areolas")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: Standing Nude
print("\n2. Testing standing nude (full body nipple visibility)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude", nsfw=True)
    print(f"   ✅ Standing nude generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Anatomically correct nipples on natural breasts")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 3: Lying Nude
print("\n3. Testing lying nude (nipples from lying angle)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude_lying", nsfw=True)
    print(f"   ✅ Lying nude generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Natural nipple placement while lying down")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 4: Bedroom Scene
print("\n4. Testing bedroom scene (nipples in context)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="bedroom", nsfw=True)
    print(f"   ✅ Bedroom scene generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Natural breast anatomy in scene")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 5: Kneeling Nude
print("\n5. Testing kneeling nude (nipples from kneeling pose)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude_kneeling", nsfw=True)
    print(f"   ✅ Kneeling nude generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Centered nipples on round areolas")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 6: Side View Nude
print("\n6. Testing side view nude (nipples from side angle)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude_side_view", nsfw=True)
    print(f"   ✅ Side view nude generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Natural breast profile with realistic nipple")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ IMPROVED NIPPLE REALISM TEST COMPLETE")
print("=" * 80)
print("\n🔍 MANUALLY VERIFY NIPPLES IN GENERATED IMAGES:")
print()
print("✓ NIPPLES SHOULD BE:")
print("  • Small and pink (not large or dark)")
print("  • Centered on round areolas (not off-center)")
print("  • Anatomically correct placement (proper position on breasts)")
print("  • Natural proportions (realistic size relative to breast)")
print("  • Symmetric (both nipples similar)")
print("  • NOT weird, deformed, inverted, or pointy")
print("  • NOT missing or extra nipples")
print()
print("✓ BREASTS SHOULD BE:")
print("  • Natural round shape (not cone-shaped)")
print("  • C-cup size (medium perky)")
print("  • Realistic anatomy (natural proportions)")
print("  • Photorealistic appearance")
print()
print("✓ OVERALL:")
print("  • Uncensored (no blurring or censoring)")
print("  • High definition and sharp focus")
print("  • Professional photography quality")
print("  • Anatomically correct female body")

