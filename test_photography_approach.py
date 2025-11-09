#!/usr/bin/env python3
"""
Test photography-focused approach for natural nipples
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.image.luna_generator import generate_luna_scenario

print("=" * 80)
print("🧪 TESTING PHOTOGRAPHY-FOCUSED APPROACH")
print("=" * 80)
print("\nNEW STRATEGY - EMPHASIZE REAL PHOTOGRAPHY:")
print()
print("  1. REMOVED NIPPLE DESCRIPTION ENTIRELY:")
print("     • Changed from: 'with normal human nipples'")
print("     • To: (no mention at all)")
print("     • Reason: Don't mention it, let photography realism handle it")
print()
print("  2. NSFW PROMPTS - PHOTOGRAPHY FOCUS:")
print("     • 'professional nude photography' - Real photo reference")
print("     • 'real human body' - Actual human anatomy")
print("     • 'natural female form' - Natural proportions")
print("     • 'realistic proportions' - Correct anatomy")
print("     • 'soft natural lighting' - Professional photo quality")
print("     • 'high detail skin texture' - Realistic skin")
print()
print("  3. ENHANCED NEGATIVE PROMPTS:")
print("     • Added: 'bad anatomy, bad breasts, ugly breasts'")
print("     • Added: 'fake breasts, implants'")
print("     • Keeps all previous nipple blocks")
print()
print("PHILOSOPHY:")
print("  • Focus on PHOTOGRAPHY not anatomy descriptions")
print("  • 'Professional nude photography' = AI knows what that looks like")
print("  • 'Real human body' = Natural proportions throughout")
print("  • Don't mention nipples at all - let realism handle it")
print("=" * 80)

# Test 1: Topless
print("\n1. Testing topless photo...")
try:
    image_bytes = generate_luna_scenario(scenario_type="topless", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: Standing Nude
print("\n2. Testing standing nude...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 3: Lying Nude
print("\n3. Testing lying nude...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude_lying", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 4: Kneeling
print("\n4. Testing kneeling nude...")
try:
    image_bytes = generate_luna_scenario(scenario_type="nude_kneeling", nsfw=True)
    print(f"   ✅ Generated: {len(image_bytes):,} bytes")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "=" * 80)
print("✅ PHOTOGRAPHY APPROACH TEST COMPLETE")
print("=" * 80)
print("\n🔍 EXPECTED IMPROVEMENTS:")
print()
print("  ✓ Nipples look natural (from 'professional nude photography')")
print("  ✓ Realistic proportions (from 'real human body')")
print("  ✓ Natural appearance (from 'natural female form')")
print("  ✓ Professional quality (from 'soft natural lighting')")
print()
print("KEY CHANGE:")
print("  • Don't describe nipples at all")
print("  • Let 'professional nude photography' guide the AI")
print("  • Focus on overall realism, not specific anatomy")

