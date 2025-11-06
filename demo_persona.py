#!/usr/bin/env python3
"""
Luna Noir Persona Engine Demo
Interactive demonstration of Luna's personality and mood adaptation
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath('.'))

from src.dialogue.persona import PersonaEngine


def print_header():
    """Print demo header"""
    print("\n" + "=" * 70)
    print("🌙 LUNA NOIR - PERSONA ENGINE DEMO")
    print("=" * 70)
    print("This demo shows how Luna's personality adapts to different messages")
    print("=" * 70 + "\n")


def demo_greetings():
    """Demo time-based greetings"""
    print("📍 DEMO 1: Time-Based Greetings")
    print("-" * 70)
    
    luna = PersonaEngine()
    
    for name in ["Alex", "Jordan", "Sam"]:
        greeting = luna.get_greeting(name)
        print(f"👤 User: {name}")
        print(f"🌙 Luna: {greeting}")
        print()


def demo_mood_adaptation():
    """Demo mood detection and adaptation"""
    print("\n📍 DEMO 2: Mood Detection & Adaptive Responses")
    print("-" * 70)
    
    luna = PersonaEngine()
    
    test_scenarios = [
        ("Affectionate", "I miss you so much, Luna 💕"),
        ("Defensive", "I'm so angry right now!"),
        ("Comforting", "I'm feeling really lonely today..."),
        ("Playful", "Haha that's hilarious! 😂"),
        ("Curious", "Why do you think that happens?"),
        ("Neutral", "Just checking in.")
    ]
    
    for scenario_name, message in test_scenarios:
        response = luna.respond(message, "Alex")
        print(f"📝 Scenario: {scenario_name}")
        print(f"👤 User: {message}")
        print(f"🌙 Luna (mood: {luna.mood}): {response}")
        print()


def demo_memory():
    """Demo conversation memory"""
    print("\n📍 DEMO 3: Conversation Memory")
    print("-" * 70)
    
    luna = PersonaEngine()
    
    conversation = [
        "Hey Luna, how are you?",
        "I've been thinking about you",
        "What do you like to do?",
        "That's really interesting!",
        "I'm feeling a bit down today"
    ]
    
    print("Having a conversation...\n")
    for i, msg in enumerate(conversation, 1):
        response = luna.respond(msg, "Alex")
        print(f"{i}. 👤 Alex: {msg}")
        print(f"   🌙 Luna: {response}")
        print()
    
    print("\n💭 Memory Recall:")
    print("-" * 70)
    print(luna.get_memory_summary())


def demo_personality_info():
    """Demo personality information"""
    print("\n📍 DEMO 4: Personality Information")
    print("-" * 70)
    
    luna = PersonaEngine()
    
    # Have a few exchanges first
    luna.respond("Hey Luna!", "Alex")
    luna.respond("You're amazing", "Alex")
    
    info = luna.get_personality_info()
    
    print(f"🌙 Name: {info['name']}")
    print(f"📦 Version: {info['version']}")
    print(f"😊 Current Mood: {info['current_mood']}")
    print(f"⚡ Energy Level: {int(info['energy_level'] * 100)}%")
    print(f"💭 Conversations Remembered: {info['memory_count']}")
    print(f"\n🎭 Personality Traits:")
    print(f"  • Base Tone: {info['personality']['base_tone']}")
    print(f"  • Temperament: {info['personality']['temperament']}")
    print(f"  • Likes: {', '.join(info['personality']['likes'])}")
    print(f"  • Dislikes: {', '.join(info['personality']['dislikes'])}")


def interactive_mode():
    """Interactive chat with Luna"""
    print("\n📍 INTERACTIVE MODE")
    print("-" * 70)
    print("Chat with Luna! Type 'quit' to exit, 'memory' to see history")
    print("-" * 70 + "\n")
    
    luna = PersonaEngine()
    user_name = input("What's your name? ").strip() or "there"
    
    print(f"\n🌙 Luna: {luna.get_greeting(user_name)}\n")
    
    while True:
        try:
            user_input = input(f"👤 {user_name}: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print(f"\n🌙 Luna: See you later, {user_name}! 💕\n")
                break
            
            if user_input.lower() == 'memory':
                print(f"\n{luna.get_memory_summary()}\n")
                continue
            
            if user_input.lower() == 'mood':
                info = luna.get_personality_info()
                print(f"\n🌙 Current mood: {info['current_mood']}")
                print(f"⚡ Energy: {int(info['energy_level'] * 100)}%\n")
                continue
            
            response = luna.respond(user_input, user_name)
            print(f"🌙 Luna: {response}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n🌙 Luna: Caught you trying to leave! Bye {user_name}! 😏\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def main():
    """Run all demos"""
    print_header()
    
    print("Choose a demo:")
    print("1. Time-Based Greetings")
    print("2. Mood Detection & Adaptive Responses")
    print("3. Conversation Memory")
    print("4. Personality Information")
    print("5. Interactive Chat Mode")
    print("6. Run All Demos (1-4)")
    print("0. Exit")
    
    choice = input("\nEnter choice (0-6): ").strip()
    
    if choice == '1':
        demo_greetings()
    elif choice == '2':
        demo_mood_adaptation()
    elif choice == '3':
        demo_memory()
    elif choice == '4':
        demo_personality_info()
    elif choice == '5':
        interactive_mode()
    elif choice == '6':
        demo_greetings()
        demo_mood_adaptation()
        demo_memory()
        demo_personality_info()
    elif choice == '0':
        print("\n👋 Goodbye!\n")
        return
    else:
        print("\n❌ Invalid choice\n")
        return
    
    print("\n" + "=" * 70)
    print("✅ Demo Complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

