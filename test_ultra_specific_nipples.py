#!/usr/bin/env python3
"""
Test ULTRA-SPECIFIC nipple definition
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.image.luna_generator import generate_luna_scenario

print("=" * 80)
print("🧪 TESTING ULTRA-SPECIFIC NIPPLE DEFINITION")
print("=" * 80)
print("\nNIPPLE IMPROVEMENTS:")
print()
print("  BASE DESCRIPTION:")
print("  • Before: 'perky C-cup breasts with soft pink nipples and small areolas'")
print("  • After:  'perky C-cup breasts with small light pink nipples centered on pale pink circular areolas 2cm diameter'")
print()
print("  NSFW PROMPTS:")
print("  • Before: 'soft pink nipples'")
print("  • After:  'small light pink nipples centered on pale pink circular areolas, realistic breast anatomy'")
print()
print("  NEGATIVE PROMPTS ADDED:")
print("  • 'large areolas' - Blocks oversized areolas")
print("  • 'brown nipples' - Blocks dark brown color")
print("  • 'red nipples' - Blocks red/irritated color")
print("  • 'puffy nipples' - Blocks puffy appearance")
print()
print("  KEY SPECIFICATIONS:")
print("  ✓ Size: 'small' (not large or oversized)")
print("  ✓ Color: 'light pink' (specific shade)")
print("  ✓ Position: 'centered on' (proper placement)")
print("  ✓ Areola color: 'pale pink' (matches skin tone)")
print("  ✓ Areola shape: 'circular' (not irregular)")
print("  ✓ Areola size: '2cm diameter' (realistic proportion)")
print("  ✓ Anatomy: 'realistic breast anatomy' (natural)")
print()
print("STRATEGY:")
print("  • Ultra-specific measurements and colors")
print("  • Explicit positioning (centered)")
print("  • Detailed areola description")
print("  • Enhanced negative prompts")
print("=" * 80)

# Test 1: Topless (primary nipple test)
print("\n1. Testing topless photo (primary nipple focus)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="topless", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Small light pink nipples centered on pale pink circular areolas")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: Standing nude (full body with nipples)
print("\n2. Testing standing nude (full body nipple view)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Small light pink nipples, 2cm pale pink areolas")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 3: Lying nude (close-up potential)
print("\n3. Testing lying nude (detailed nipple view)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude_lying", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Centered small light pink nipples on circular areolas")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 4: Kneeling nude (angle test)
print("\n4. Testing kneeling nude (angle consistency)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude_kneeling", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Small light pink nipples, pale pink 2cm areolas")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 5: Sitting nude (natural position)
print("\n5. Testing sitting nude (natural nipple position)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude_sitting", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
    print(f"   → Check: Centered small light pink nipples on pale pink circular areolas")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ ULTRA-SPECIFIC NIPPLE DEFINITION TEST COMPLETE")
print("=" * 80)
print("\n🔍 EXPECTED RESULTS:")
print()
print("NIPPLE SPECIFICATIONS:")
print("  ✓ Size: Small (not large)")
print("  ✓ Color: Light pink (not dark, brown, or red)")
print("  ✓ Position: Centered on areolas (not off-center)")
print("  ✓ Shape: Natural (not pointy or puffy)")
print()
print("AREOLA SPECIFICATIONS:")
print("  ✓ Size: 2cm diameter (realistic proportion)")
print("  ✓ Color: Pale pink (matches pale skin)")
print("  ✓ Shape: Circular (not irregular or oval)")
print("  ✓ Position: Centered on breasts")
print()
print("OVERALL:")
print("  ✓ Realistic breast anatomy")
print("  ✓ Professional nude photography quality")
print("  ✓ Natural lighting")
print("  ✓ Photorealistic appearance")
print()
print("KEY IMPROVEMENTS:")
print("  • Added specific size: 'small'")
print("  • Added specific color: 'light pink' (nipples) + 'pale pink' (areolas)")
print("  • Added positioning: 'centered on'")
print("  • Added shape: 'circular'")
print("  • Added measurement: '2cm diameter'")
print("  • Added anatomy note: 'realistic breast anatomy'")
print("  • Blocked variations: large areolas, brown/red nipples, puffy nipples")

