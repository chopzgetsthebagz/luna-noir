#!/usr/bin/env python3
"""
Quick test to verify bot structure without running the server
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath('.'))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from src.core.bot import LunaNoirBot, create_bot
        print("✓ src.core.bot imported successfully")
    except Exception as e:
        print(f"✗ Failed to import src.core.bot: {e}")
        return False
    
    try:
        from src.server import app
        print("✓ src.server.app imported successfully")
    except Exception as e:
        print(f"✗ Failed to import src.server.app: {e}")
        return False
    
    return True

def test_bot_creation():
    """Test bot creation with dummy token"""
    print("\nTesting bot creation...")

    try:
        from src.core.bot import create_bot

        # Create bot with dummy token (won't connect, just test structure)
        bot = create_bot("123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
        print("✓ Bot instance created successfully")

        # Check bot has required methods
        required_methods = [
            'start_command',
            'menu_command',
            'help_command',
            'mood_command',
            'memory_command',
            'handle_message',
            'process_update',
            'set_webhook',
            'get_webhook_info'
        ]

        for method in required_methods:
            if hasattr(bot, method):
                print(f"✓ Bot has method: {method}")
            else:
                print(f"✗ Bot missing method: {method}")
                return False

        # Check persona integration
        if hasattr(bot, 'persona'):
            print("✓ Bot has PersonaEngine integrated")
            print(f"  - Persona name: {bot.persona.name}")
            print(f"  - Persona version: {bot.persona.version}")
        else:
            print("✗ Bot missing PersonaEngine")
            return False

        return True

    except Exception as e:
        print(f"✗ Failed to create bot: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_flask_app():
    """Test Flask app structure"""
    print("\nTesting Flask app...")
    
    try:
        from src.server.app import app
        
        # Check routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        print(f"✓ Flask app has {len(routes)} routes:")
        for route in routes:
            print(f"  - {route}")
        
        required_routes = ['/', '/webhook', '/health', '/webhook/info']
        for route in required_routes:
            if route in routes:
                print(f"✓ Required route exists: {route}")
            else:
                print(f"✗ Missing required route: {route}")
                return False
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to test Flask app: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_persona_engine():
    """Test PersonaEngine functionality"""
    print("\nTesting PersonaEngine...")

    try:
        from src.dialogue.persona import PersonaEngine

        # Create persona instance
        persona = PersonaEngine()
        print("✓ PersonaEngine created successfully")

        # Test greeting
        greeting = persona.get_greeting("TestUser")
        print(f"✓ Greeting generated: {greeting[:50]}...")

        # Test response generation
        test_messages = [
            ("I love you", "affectionate"),
            ("I'm so sad", "comforting"),
            ("Haha that's funny", "playful"),
            ("Why is that?", "curious")
        ]

        for msg, expected_mood in test_messages:
            response = persona.respond(msg, "TestUser")
            if persona.mood == expected_mood:
                print(f"✓ Mood detection: '{msg}' → {expected_mood}")
            else:
                print(f"⚠ Mood detection: '{msg}' → {persona.mood} (expected {expected_mood})")

        # Test memory
        if len(persona.memory) > 0:
            print(f"✓ Memory working: {len(persona.memory)} exchanges stored")
        else:
            print("✗ Memory not working")
            return False

        # Test memory recall
        recalled = persona.recall(2)
        print(f"✓ Memory recall: {len(recalled)} exchanges retrieved")

        return True

    except Exception as e:
        print(f"✗ Failed to test PersonaEngine: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Luna Noir Bot - Structure Test")
    print("=" * 60)

    results = []

    results.append(("Imports", test_imports()))
    results.append(("PersonaEngine", test_persona_engine()))
    results.append(("Bot Creation", test_bot_creation()))
    results.append(("Flask App", test_flask_app()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())

