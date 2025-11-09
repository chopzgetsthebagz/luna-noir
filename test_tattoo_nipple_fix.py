#!/usr/bin/env python3
"""
Test improved tattoo consistency and better nipples
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.image.luna_generator import generate_luna_scenario

print("=" * 80)
print("🧪 TESTING IMPROVED TATTOO CONSISTENCY + BETTER NIPPLES")
print("=" * 80)
print("\nDUAL IMPROVEMENTS:")
print()
print("  1. TATTOO CONSISTENCY:")
print("     • Changed: 'exactly one small minimalist black outline snake tattoo on outer right forearm 10cm below elbow'")
print("     • To: 'single small simple black line art snake tattoo on right forearm only no other tattoos'")
print("     • Added to prompts: 'single small snake tattoo on right forearm only'")
print("     • Reason: Simpler, more direct language for consistency")
print()
print("  2. BETTER NIPPLES:")
print("     • Changed: 'perky medium C-cup natural breasts'")
print("     • To: 'perky C-cup breasts with soft pink nipples and small areolas'")
print("     • Added to NSFW prompts: 'soft pink nipples, realistic breast proportions'")
print("     • Reason: Specific but natural description")
print()
print("  3. ENHANCED NEGATIVE PROMPTS:")
print("     • Tattoos: 'many tattoos, multiple tattoos, face tattoos, neck tattoos, chest tattoos, breast tattoos, stomach tattoos, back tattoos, leg tattoos, sleeve tattoos, arm sleeve, full sleeve, colorful tattoos, large tattoos'")
print("     • Nipples: 'dark nipples, bolt-on breasts' (added)")
print()
print("STRATEGY:")
print("  • Tattoo: Simple direct language + reinforce in prompts")
print("  • Nipples: Describe as 'soft pink nipples and small areolas'")
print("  • Both: Strong negative prompts to block variations")
print("=" * 80)

# Test 1: Topless (shows nipples clearly)
print("\n1. Testing topless photo (nipple focus)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="topless", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Soft pink nipples, small areolas")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: Full body (shows tattoo)
print("\n2. Testing full body shot (tattoo visibility)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="fullbody", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Single small snake tattoo on right forearm only")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 3: Standing nude (both nipples and tattoo)
print("\n3. Testing standing nude (both features)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Soft pink nipples + single snake tattoo")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 4: Lying nude (nipple detail)
print("\n4. Testing lying nude (nipple detail)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude_lying", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Soft pink nipples with small areolas")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 5: Mirror selfie (tattoo check)
print("\n5. Testing mirror selfie (tattoo consistency)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="mirror", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Only one small snake tattoo on right forearm")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ TATTOO + NIPPLE IMPROVEMENT TEST COMPLETE")
print("=" * 80)
print("\n🔍 EXPECTED RESULTS:")
print()
print("TATTOOS:")
print("  ✓ Single small simple black snake tattoo")
print("  ✓ On right forearm only")
print("  ✓ No other tattoos anywhere")
print("  ✓ Consistent across all images")
print()
print("NIPPLES:")
print("  ✓ Soft pink color (not dark or weird)")
print("  ✓ Small areolas (realistic proportions)")
print("  ✓ Natural appearance (not deformed)")
print("  ✓ Consistent size and shape")
print()
print("KEY CHANGES:")
print("  • Tattoo: Simpler language + reinforced in prompts")
print("  • Nipples: Specific 'soft pink nipples and small areolas'")
print("  • Both: Strong negative prompts blocking variations")

