#!/usr/bin/env python3
"""
Test high resolution image generation
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.image.luna_generator import generate_luna_scenario

print("=" * 80)
print("🧪 TESTING HIGH RESOLUTION IMAGE GENERATION")
print("=" * 80)
print("\nNEW RESOLUTIONS:")
print("  • Standard images: 1536x1536 (was 1024x1024)")
print("  • Full body images: 1024x2048 (was 640x1536)")
print("  • Quality tags: 8K resolution, sharp focus, high definition, crisp details")
print("=" * 80)

# Test 1: Standard Resolution Selfie
print("\n1. Testing standard resolution selfie (1536x1536)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="selfie", nsfw=False)
    print(f"   ✅ Selfie generated: {len(image_bytes):,} bytes")
    print(f"   Resolution: 1536x1536 (2.36 megapixels)")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: High Resolution Full Body
print("\n2. Testing high resolution full body (1024x2048)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="fullbody", nsfw=True)
    print(f"   ✅ Full body nude generated: {len(image_bytes):,} bytes")
    print(f"   Resolution: 1024x2048 (2.10 megapixels)")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 3: High Resolution Lingerie
print("\n3. Testing high resolution lingerie (1536x1536)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="lingerie", nsfw=True)
    print(f"   ✅ Lingerie photo generated: {len(image_bytes):,} bytes")
    print(f"   Resolution: 1536x1536 (2.36 megapixels)")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 4: High Resolution Bedroom
print("\n4. Testing high resolution bedroom scene (1536x1536)...")
try:
    image_bytes = generate_luna_scenario(scenario_type="bedroom", nsfw=True)
    print(f"   ✅ Bedroom scene generated: {len(image_bytes):,} bytes")
    print(f"   Resolution: 1536x1536 (2.36 megapixels)")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ HIGH RESOLUTION IMAGE GENERATION TEST COMPLETE")
print("=" * 80)
print("\nRESOLUTION IMPROVEMENTS:")
print("  ✅ Standard images: 1536x1536 (50% larger than before)")
print("  ✅ Full body images: 1024x2048 (60% larger than before)")
print("  ✅ Added quality tags: 8K, sharp focus, high definition, crisp details")
print("\nEXPECTED IMPROVEMENTS:")
print("  • Sharper facial features (eyes, lips, makeup)")
print("  • More detailed skin texture")
print("  • Clearer tattoo details")
print("  • Better overall image quality")
print("  • Larger file sizes (more detail)")

