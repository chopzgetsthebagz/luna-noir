#!/usr/bin/env python3
"""
Test GIF Generation for Luna Noir
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.image.gif_generator import generate_luna_gif, get_available_gifs

print("=" * 80)
print("🎬 TESTING ANIMATED GIF GENERATION")
print("=" * 80)

# Show available GIFs
print("\n📋 AVAILABLE GIF SCENARIOS:")
print()

sfw_gifs = get_available_gifs(nsfw=False)
nsfw_gifs = get_available_gifs(nsfw=True)

print("SFW GIFs:")
for key, info in sfw_gifs.items():
    print(f"  • {key}: {info['name']} ({info['frames']} frames, {info['duration']}ms/frame)")

print("\nNSFW GIFs:")
for key, info in nsfw_gifs.items():
    if key not in sfw_gifs:
        print(f"  • {key}: {info['name']} ({info['frames']} frames, {info['duration']}ms/frame)")

print("\n" + "=" * 80)
print("🧪 TESTING GIF GENERATION (WINK)")
print("=" * 80)

# Test wink GIF (SFW, smallest - 5 frames)
print("\n1. Testing 'wink' GIF (5 frames, SFW)...")
try:
    gif_bytes, gif_name = generate_luna_gif(scenario_type="wink", nsfw=False)
    print(f"   ✅ Generated: {gif_name}")
    print(f"   📦 Size: {len(gif_bytes):,} bytes ({len(gif_bytes) / 1024 / 1024:.2f} MB)")
    
    # Save to file for inspection
    output_path = Path("test_wink.gif")
    output_path.write_bytes(gif_bytes)
    print(f"   💾 Saved to: {output_path}")
    
except Exception as e:
    print(f"   ❌ Failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("✅ GIF GENERATION TEST COMPLETE")
print("=" * 80)
print()
print("🎯 NEXT STEPS:")
print("  1. Check test_wink.gif to verify animation quality")
print("  2. Test other GIF types if wink works")
print("  3. Deploy to bot for user testing")
print()
print("📝 GIF FEATURES:")
print("  ✓ Multiple animation types (wink, kiss, pose, dance, rotate)")
print("  ✓ NSFW support (tease, undress, nude poses)")
print("  ✓ 3-8 frames per GIF")
print("  ✓ 400-600ms per frame (smooth animation)")
print("  ✓ Automatic frame generation from Luna images")
print("  ✓ Optimized GIF creation with PIL")

