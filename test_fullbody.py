#!/usr/bin/env python3
"""
Test full body image generation to verify it shows head to toe
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.image.luna_generator import generate_luna_scenario

print("=" * 80)
print("🧪 TESTING FULL BODY IMAGE GENERATION")
print("=" * 80)

# Test 1: SFW Full Body
print("\n1. Testing SFW full body shot...")
try:
    image_bytes = generate_luna_scenario(scenario_type="fullbody", nsfw=False)
    print(f"   ✅ SFW full body generated: {len(image_bytes)} bytes")
    print(f"   Expected: Head to toe, clothed, standing pose")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: NSFW Full Body
print("\n2. Testing NSFW full body nude...")
try:
    image_bytes = generate_luna_scenario(scenario_type="fullbody", nsfw=True)
    print(f"   ✅ NSFW full body generated: {len(image_bytes)} bytes")
    print(f"   Expected: Head to toe, completely naked, full frontal")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 3: Standing Nude
print("\n3. Testing standing nude pose...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude", nsfw=True)
    print(f"   ✅ Standing nude generated: {len(image_bytes)} bytes")
    print(f"   Expected: Full body visible from head to toe")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ FULL BODY IMAGE GENERATION TEST COMPLETE")
print("=" * 80)
print("\nCheck the generated images to verify:")
print("  - Entire body visible from head to toe")
print("  - No cropping at feet or head")
print("  - Consistent Luna appearance")
print("  - Proper aspect ratio (taller for full body)")

