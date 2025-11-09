#!/usr/bin/env python3
"""
Test natural face and nipple improvements
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.image.luna_generator import generate_luna_scenario

print("=" * 80)
print("🧪 TESTING NATURAL FEATURES - FACE & NIPPLES")
print("=" * 80)
print("\nIMPROVEMENTS MADE:")
print("  1. FACE:")
print("     • Added 'natural skin texture with visible pores'")
print("     • Added 'photorealistic human features'")
print("     • Added 'realistic face'")
print("     • Negative: 'pixelated, censored, blurred face, plastic skin, doll face'")
print("     • Negative: 'artificial, fake skin, smooth skin, airbrushed'")
print()
print("  2. NIPPLES:")
print("     • Added 'small pink nipples and natural areolas' to base description")
print("     • Added 'natural breast anatomy with realistic nipples and areolas'")
print("     • Added 'uncensored' to NSFW prompts")
print("     • Negative: 'deformed nipples, missing nipples, extra nipples'")
print("=" * 80)

# Test 1: Topless Photo (nipple test)
print("\n1. Testing topless photo (nipple visibility & realism)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="topless", nsfw=True)
    print(f"   ✅ Topless photo generated: {len(image_bytes):,} bytes")
    print(f"   → Should show: Natural pink nipples with realistic areolas")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: Standing Nude (full body nipple test)
print("\n2. Testing standing nude (full body with natural nipples)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude", nsfw=True)
    print(f"   ✅ Standing nude generated: {len(image_bytes):,} bytes")
    print(f"   → Should show: Complete body with natural nipples visible")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 3: Selfie (face realism test)
print("\n3. Testing selfie (natural face with skin texture)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="selfie", nsfw=False)
    print(f"   ✅ Selfie generated: {len(image_bytes):,} bytes")
    print(f"   → Should show: Natural skin with visible pores, realistic face")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 4: Bedroom Scene (overall natural appearance)
print("\n4. Testing bedroom scene (natural face + body)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="bedroom", nsfw=True)
    print(f"   ✅ Bedroom scene generated: {len(image_bytes):,} bytes")
    print(f"   → Should show: Natural skin texture, realistic face, natural nipples")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 5: Lingerie (face detail test)
print("\n5. Testing lingerie photo (face detail & skin texture)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="lingerie", nsfw=True)
    print(f"   ✅ Lingerie photo generated: {len(image_bytes):,} bytes")
    print(f"   → Should show: Detailed face with natural skin, visible pores")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 6: Bent Over Nude (nipple angle test)
print("\n6. Testing bent over nude (nipples from different angle)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude_bent_over", nsfw=True)
    print(f"   ✅ Bent over nude generated: {len(image_bytes):,} bytes")
    print(f"   → Should show: Natural nipples visible from bent over angle")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ NATURAL FEATURES TEST COMPLETE")
print("=" * 80)
print("\n🔍 MANUALLY VERIFY THE GENERATED IMAGES:")
print()
print("📸 FACE SHOULD LOOK:")
print("  ✓ Natural skin texture with visible pores (not plastic/smooth)")
print("  ✓ Realistic human features (not doll-like or artificial)")
print("  ✓ Sharp facial details (eyes, lips, makeup clearly defined)")
print("  ✓ NOT pixelated or blurred")
print("  ✓ NOT overly airbrushed or smoothed")
print()
print("🎨 NIPPLES SHOULD LOOK:")
print("  ✓ Small pink nipples clearly visible")
print("  ✓ Natural areolas (realistic size and color)")
print("  ✓ Proper breast anatomy (natural proportions)")
print("  ✓ NOT deformed, missing, or extra nipples")
print("  ✓ NOT censored or blurred")
print("  ✓ Uncensored and realistic")
print()
print("💡 OVERALL APPEARANCE:")
print("  ✓ Photorealistic human (not cartoon or 3D render)")
print("  ✓ Natural skin with texture and pores")
print("  ✓ Realistic lighting and shadows")
print("  ✓ Professional photography quality")
print("  ✓ High definition and sharp focus")

