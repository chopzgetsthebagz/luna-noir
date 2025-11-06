#!/usr/bin/env python3
"""
Interactive demo for Luna Noir with Ollama integration
Chat with Luna in your terminal!
"""

import sys
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings/errors for cleaner output
    format='%(levelname)s - %(message)s'
)

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.dialogue.persona_engine import PersonaEngine


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*60)
    print("🌙 LUNA NOIR - Interactive Chat Demo")
    print("="*60)
    print()


def print_status(persona):
    """Print current status"""
    if persona.use_ollama:
        print("✓ AI Mode: Ollama (Local AI)")
        print(f"  Model: {persona.ollama_client.model}")
    else:
        print("⚠ AI Mode: Template Responses (Ollama not available)")
    print()


def print_help():
    """Print help message"""
    print("\nCommands:")
    print("  /help     - Show this help")
    print("  /mood     - Show current mood")
    print("  /memory   - Show conversation memory")
    print("  /clear    - Clear conversation memory")
    print("  /info     - Show personality info")
    print("  /quit     - Exit the demo")
    print()


def main():
    """Run interactive demo"""
    print_banner()

    # Set model from .env if available
    from dotenv import load_dotenv
    load_dotenv()

    # Create PersonaEngine
    print("Initializing Luna Noir...")
    persona = PersonaEngine(use_ollama=True)
    print()
    
    print_status(persona)
    
    # Get user name
    user_name = input("What's your name? ").strip() or "there"
    print()
    
    # Greeting
    greeting = persona.get_greeting(user_name)
    print(f"Luna: {greeting}")
    print()
    
    print("Type /help for commands or just start chatting!")
    print("-" * 60)
    print()
    
    # Chat loop
    while True:
        try:
            # Get user input
            user_input = input(f"{user_name}: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == "/quit":
                print("\nLuna: See you later! 🌙")
                break
            
            elif user_input.lower() == "/help":
                print_help()
                continue
            
            elif user_input.lower() == "/mood":
                print(f"\nCurrent mood: {persona.mood}")
                print()
                continue
            
            elif user_input.lower() == "/memory":
                print("\n" + persona.get_memory_summary())
                print()
                continue
            
            elif user_input.lower() == "/clear":
                persona.clear_memory()
                print("\n✓ Memory cleared")
                print()
                continue
            
            elif user_input.lower() == "/info":
                info = persona.get_personality_info()
                print(f"\nName: {info['name']}")
                print(f"Version: {info['version']}")
                print(f"Current Mood: {info['current_mood']}")
                print(f"Energy Level: {info['energy_level']}")
                print(f"Memory Count: {info['memory_count']}")
                print(f"Personality: {info['personality']}")
                print()
                continue
            
            # Generate response
            print()  # Blank line before response
            response = persona.respond(user_input, user_name)
            print(f"Luna ({persona.mood}): {response}")
            print()
            
        except KeyboardInterrupt:
            print("\n\nLuna: Leaving so soon? 😏")
            break
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
            break
    
    print("\nThanks for chatting! 💕")


if __name__ == "__main__":
    main()

