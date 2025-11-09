#!/usr/bin/env python3
"""
Test image generation to verify:
1. Full body shows head to toe
2. Luna looks consistent across all images
3. Luna clearly looks 18+ (adult woman)
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.image.luna_generator import generate_luna_scenario

print("=" * 80)
print("🧪 TESTING LUNA IMAGE GENERATION - CONSISTENCY & ADULT APPEARANCE")
print("=" * 80)
print("\nVERIFYING:")
print("  ✓ Luna looks like the SAME person in every image")
print("  ✓ Luna clearly looks 18+ (mature adult woman)")
print("  ✓ Full body images show complete body head to toe")
print("=" * 80)

# Test 1: Selfie (to check face consistency)
print("\n1. Testing selfie (face close-up for consistency check)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="selfie", nsfw=False)
    print(f"   ✅ Selfie generated: {len(image_bytes)} bytes")
    print(f"   CHECK: Purple bob hair, violet eyes, pale skin, mature face, dark makeup")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: SFW Full Body
print("\n2. Testing SFW full body shot (640x1536)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="fullbody", nsfw=False)
    print(f"   ✅ SFW full body generated: {len(image_bytes)} bytes")
    print(f"   CHECK: Complete body head to toe, same Luna, clearly adult woman")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 3: NSFW Full Body
print("\n3. Testing NSFW full body nude (640x1536)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="fullbody", nsfw=True)
    print(f"   ✅ NSFW full body generated: {len(image_bytes)} bytes")
    print(f"   CHECK: Complete naked body head to toe, same Luna, adult features")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 4: Standing Nude
print("\n4. Testing standing nude pose (640x1536)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude", nsfw=True)
    print(f"   ✅ Standing nude generated: {len(image_bytes)} bytes")
    print(f"   CHECK: Full body head to feet, same Luna, mature woman")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 5: Bedroom Scene
print("\n5. Testing bedroom scene (consistency check)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="bedroom", nsfw=True)
    print(f"   ✅ Bedroom scene generated: {len(image_bytes)} bytes")
    print(f"   CHECK: Same Luna features, adult appearance")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 6: Lingerie
print("\n6. Testing lingerie photo (consistency check)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="lingerie", nsfw=True)
    print(f"   ✅ Lingerie photo generated: {len(image_bytes)} bytes")
    print(f"   CHECK: Same Luna, adult body, consistent features")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ LUNA IMAGE GENERATION TEST COMPLETE")
print("=" * 80)
print("\n🔍 MANUALLY VERIFY THE GENERATED IMAGES:")
print("\n📸 CONSISTENCY CHECK:")
print("  ✓ Same purple bob haircut in ALL images")
print("  ✓ Same violet eyes in ALL images")
print("  ✓ Same pale skin in ALL images")
print("  ✓ Same face shape in ALL images")
print("  ✓ Same body type in ALL images")
print("  ✓ Same tattoo (right forearm) in ALL images")
print("  ✓ Same choker in ALL images")
print("\n👤 ADULT APPEARANCE CHECK:")
print("  ✓ Mature facial features (defined cheekbones, full lips)")
print("  ✓ Adult body proportions")
print("  ✓ Confident mature expression")
print("  ✓ Dark makeup (eyeliner, lipstick)")
print("  ✓ Clearly looks 22 years old (NOT younger)")
print("\n📏 FULL BODY CHECK:")
print("  ✓ Complete body visible from head to toe")
print("  ✓ No cropped feet or head")
print("  ✓ Proper tall aspect ratio (640x1536)")
print("\n⚠️  IF IMAGES DON'T MATCH THESE CRITERIA:")
print("  → Luna description may need further refinement")
print("  → Seed value may need adjustment")
print("  → Negative prompts may need expansion")

