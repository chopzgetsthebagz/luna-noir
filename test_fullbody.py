#!/usr/bin/env python3
"""
Test image generation to verify:
1. Full body shows head to toe
2. Luna looks consistent across all images (face, tattoo, body)
3. Luna clearly looks 18+ (adult woman with sexy proportions)
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.image.luna_generator import generate_luna_scenario

print("=" * 80)
print("🧪 TESTING LUNA - SEXY BODY + MAXIMUM CONSISTENCY")
print("=" * 80)
print("\nVERIFYING:")
print("  ✓ Luna has sexy hourglass figure (C-cup, wide hips, bubble butt, thick thighs)")
print("  ✓ EXACT same face in every image (heart-shaped, high cheekbones, violet eyes)")
print("  ✓ EXACT same tattoo placement (one small snake on outer right forearm)")
print("  ✓ EXACT same hair (lavender purple bob with straight bangs)")
print("  ✓ Full body images show complete body head to toe")
print("=" * 80)

# Test 1: Selfie (to check face consistency)
print("\n1. Testing selfie (FACE CONSISTENCY CHECK)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="selfie", nsfw=False)
    print(f"   ✅ Selfie generated: {len(image_bytes)} bytes")
    print(f"   CHECK: Heart-shaped face, high cheekbones, violet almond eyes, winged eyeliner")
    print(f"   CHECK: Purple bob with straight bangs, plum lips, pale skin, choker")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: SFW Full Body
print("\n2. Testing SFW full body shot (BODY CONSISTENCY CHECK)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="fullbody", nsfw=False)
    print(f"   ✅ SFW full body generated: {len(image_bytes)} bytes")
    print(f"   CHECK: Hourglass figure, C-cup breasts, narrow waist, wide hips")
    print(f"   CHECK: Complete body head to toe, same face, one tattoo on right forearm")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 3: NSFW Full Body
print("\n3. Testing NSFW full body nude (SEXY BODY CHECK)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="fullbody", nsfw=True)
    print(f"   ✅ NSFW full body generated: {len(image_bytes)} bytes")
    print(f"   CHECK: Perky C-cup breasts, flat toned stomach, wide hips, bubble butt")
    print(f"   CHECK: Thick thighs, long legs, complete body head to toe")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 4: Standing Nude
print("\n4. Testing standing nude pose (TATTOO CONSISTENCY CHECK)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude", nsfw=True)
    print(f"   ✅ Standing nude generated: {len(image_bytes)} bytes")
    print(f"   CHECK: ONE small snake tattoo on outer RIGHT forearm (10cm below elbow)")
    print(f"   CHECK: No other tattoos anywhere else on body")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 5: Bedroom Scene
print("\n5. Testing bedroom scene (OVERALL CONSISTENCY CHECK)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="bedroom", nsfw=True)
    print(f"   ✅ Bedroom scene generated: {len(image_bytes)} bytes")
    print(f"   CHECK: Same face, same body, same tattoo, same hair")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 6: Lingerie
print("\n6. Testing lingerie photo (CURVES CHECK)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="lingerie", nsfw=True)
    print(f"   ✅ Lingerie photo generated: {len(image_bytes)} bytes")
    print(f"   CHECK: Sexy hourglass curves visible, C-cup cleavage, wide hips")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 7: Bent Over Nude
print("\n7. Testing bent over nude (BUTT CHECK)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude_bent_over", nsfw=True)
    print(f"   ✅ Bent over nude generated: {len(image_bytes)} bytes")
    print(f"   CHECK: Round firm bubble butt, thick thighs visible")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ LUNA IMAGE GENERATION TEST COMPLETE")
print("=" * 80)
print("\n🔍 MANUALLY VERIFY THE GENERATED IMAGES:")
print("\n📸 FACE CONSISTENCY (MUST BE IDENTICAL IN ALL IMAGES):")
print("  ✓ Heart-shaped face with high defined cheekbones")
print("  ✓ Almond-shaped bright violet purple eyes")
print("  ✓ Thick black winged eyeliner")
print("  ✓ Full pouty lips with dark plum lipstick")
print("  ✓ Lavender purple bob with perfectly straight bangs across forehead")
print("  ✓ Very pale porcelain white skin")
print("  ✓ Thin black leather choker around neck")
print("  ✓ Seductive confident expression with sultry gaze")
print("\n🎨 TATTOO CONSISTENCY (CRITICAL - MUST BE EXACT):")
print("  ✓ EXACTLY ONE small minimalist black outline snake tattoo")
print("  ✓ Located on OUTER RIGHT FOREARM, 10cm below elbow")
print("  ✓ NO other tattoos anywhere else on body")
print("  ✓ NO face tattoos, chest tattoos, back tattoos, or sleeve tattoos")
print("\n💃 SEXY BODY (HOURGLASS FIGURE):")
print("  ✓ Perky medium C-cup breasts")
print("  ✓ Narrow waist with flat toned stomach (subtle abs)")
print("  ✓ Wide feminine hips")
print("  ✓ Round firm bubble butt")
print("  ✓ Thick toned thighs")
print("  ✓ Long shapely legs")
print("  ✓ Athletic curvy body type (168cm / 5'6\")")
print("\n📏 FULL BODY CHECK:")
print("  ✓ Complete body visible from head to toe")
print("  ✓ No cropped feet or head")
print("  ✓ Proper tall aspect ratio (640x1536)")
print("\n⚠️  IF IMAGES DON'T MATCH THESE EXACT CRITERIA:")
print("  → Face should be IDENTICAL in every image")
print("  → Tattoo should be in EXACT same spot (outer right forearm)")
print("  → Body should have sexy hourglass proportions")
print("  → If inconsistent, seed or description needs adjustment")

