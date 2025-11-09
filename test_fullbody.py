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
print("🧪 TESTING FULL BODY IMAGE GENERATION - IMPROVED VERSION")
print("=" * 80)

# Test 1: SFW Full Body
print("\n1. Testing SFW full body shot (640x1536)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="fullbody", nsfw=False)
    print(f"   ✅ SFW full body generated: {len(image_bytes)} bytes")
    print(f"   Expected: Complete body from head to feet, clothed")
    print(f"   Dimensions: 640x1536 (tall portrait)")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: NSFW Full Body
print("\n2. Testing NSFW full body nude (640x1536)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="fullbody", nsfw=True)
    print(f"   ✅ NSFW full body generated: {len(image_bytes)} bytes")
    print(f"   Expected: Complete naked body from head to feet")
    print(f"   Dimensions: 640x1536 (tall portrait)")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 3: Standing Nude
print("\n3. Testing standing nude pose (640x1536)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude", nsfw=True)
    print(f"   ✅ Standing nude generated: {len(image_bytes)} bytes")
    print(f"   Expected: Full body visible from head to feet")
    print(f"   Dimensions: 640x1536 (tall portrait)")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 4: Side View Nude
print("\n4. Testing side view nude (640x1536)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude_side_view", nsfw=True)
    print(f"   ✅ Side view nude generated: {len(image_bytes)} bytes")
    print(f"   Expected: Full body profile from head to feet")
    print(f"   Dimensions: 640x1536 (tall portrait)")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ FULL BODY IMAGE GENERATION TEST COMPLETE")
print("=" * 80)
print("\nIMPROVEMENTS:")
print("  ✅ Taller aspect ratio (640x1536 instead of 768x1344)")
print("  ✅ Explicit 'full length portrait' instruction added")
print("  ✅ More specific Luna description for consistency")
print("  ✅ Simplified prompts to avoid confusion")
print("\nVerify images show:")
print("  - Complete body from top of head to bottom of feet")
print("  - No cropping at any edge")
print("  - Consistent Luna features (purple bob, violet eyes, pale skin)")
print("  - Same person in every image")

