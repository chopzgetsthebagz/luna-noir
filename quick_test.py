#!/usr/bin/env python3
"""
Quick test of Ollama integration with phi3:mini
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Set to use phi3:mini
os.environ['OLLAMA_MODEL'] = 'phi3:mini'

from src.dialogue.persona_engine import PersonaEngine

print("="*60)
print("QUICK OLLAMA TEST - Using phi3:mini")
print("="*60)
print()

# Create persona
print("Creating PersonaEngine...")
luna = PersonaEngine(use_ollama=True)
print(f"✓ Created: {luna.name} {luna.version}")
print(f"  Ollama enabled: {luna.use_ollama}")
print()

# Test a simple message
print("Testing AI response...")
print()
user_message = "Hey Luna!"
print(f"User: {user_message}")
print()

response = luna.respond(user_message, "Alex")
print(f"Luna ({luna.mood}): {response}")
print()

if luna.use_ollama and response:
    print("✅ SUCCESS! Ollama integration is working!")
else:
    print("⚠️  Using fallback responses (Ollama not available)")

print()
print("="*60)

