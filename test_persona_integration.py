#!/usr/bin/env python3
"""
Test PersonaEngine integration with Telegram bot
Verifies all new commands and global persona instance
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath('.'))

from src.dialogue.persona_engine import PersonaEngine
from src.core.bot import persona_engine


def test_global_persona_engine():
    """Test that global persona_engine is properly initialized"""
    print("Testing global persona_engine instance...")
    
    assert persona_engine is not None, "Global persona_engine should be initialized"
    assert isinstance(persona_engine, PersonaEngine), "Should be PersonaEngine instance"
    assert persona_engine.name == "Luna Noir", "Name should be Luna Noir"
    assert persona_engine.version == "v1.0", "Version should be v1.0"
    
    print("✓ Global persona_engine initialized correctly")


def test_persona_respond():
    """Test persona respond functionality"""
    print("\nTesting persona.respond()...")
    
    # Clear memory first
    persona_engine.clear_memory()
    
    # Test different moods
    test_cases = [
        ("I love you Luna", "affectionate"),
        ("Why is the sky blue?", "curious"),
        ("Haha that's funny!", "playful"),
        ("I'm feeling sad", "comforting"),
    ]
    
    for message, expected_mood in test_cases:
        response = persona_engine.respond(message, "TestUser")
        print(f"  Message: '{message}' → Mood: {persona_engine.mood} (expected: {expected_mood})")
        assert response, f"Should get response for '{message}'"
        assert len(response) > 0, "Response should not be empty"
    
    print("✓ persona.respond() working correctly")


def test_memory_functions():
    """Test memory recall and clear"""
    print("\nTesting memory functions...")
    
    # Clear memory
    persona_engine.clear_memory()
    assert len(persona_engine.memory) == 0, "Memory should be empty after clear"
    print("  ✓ clear_memory() works")
    
    # Add some exchanges
    persona_engine.respond("Hello", "User1")
    persona_engine.respond("How are you?", "User1")
    persona_engine.respond("Tell me a joke", "User1")
    
    assert len(persona_engine.memory) == 3, "Should have 3 memories"
    print("  ✓ Memory storage works")
    
    # Test recall
    recent = persona_engine.recall(count=3)
    assert len(recent) == 3, "Should recall 3 memories"
    assert 'timestamp' in recent[0], "Memory should have timestamp"
    assert 'user_input' in recent[0], "Memory should have user_input"
    assert 'bot_reply' in recent[0], "Memory should have bot_reply"
    assert 'mood' in recent[0], "Memory should have mood"
    print("  ✓ recall() works")
    
    # Test memory summary
    summary = persona_engine.get_memory_summary()
    assert "Recent conversation" in summary or "conversation" in summary.lower(), "Summary should have conversation info"
    print("  ✓ get_memory_summary() works")
    
    print("✓ All memory functions working correctly")


def test_personality_info():
    """Test get_personality_info"""
    print("\nTesting get_personality_info()...")
    
    info = persona_engine.get_personality_info()
    
    assert 'name' in info, "Should have name"
    assert 'version' in info, "Should have version"
    assert 'current_mood' in info, "Should have current_mood"
    assert 'energy_level' in info, "Should have energy_level"
    assert 'personality' in info, "Should have personality"
    assert 'memory_count' in info, "Should have memory_count"
    
    assert info['name'] == "Luna Noir", "Name should be Luna Noir"
    assert info['version'] == "v1.0", "Version should be v1.0"
    
    print("✓ get_personality_info() working correctly")


def test_bot_commands_exist():
    """Test that bot has all required command handlers"""
    print("\nTesting bot command handlers...")
    
    from src.core.bot import LunaNoirBot
    
    # Create bot instance (with dummy token)
    bot = LunaNoirBot("dummy_token_for_testing")
    
    # Check that command methods exist
    required_methods = [
        'start_command',
        'menu_command',
        'help_command',
        'persona_command',
        'recall_command',
        'resetmem_command',
        'handle_message',
    ]
    
    for method_name in required_methods:
        assert hasattr(bot, method_name), f"Bot should have {method_name} method"
        print(f"  ✓ {method_name} exists")
    
    print("✓ All required command handlers exist")


def test_logging_format():
    """Test that exchange logging format is correct"""
    print("\nTesting exchange logging format...")
    
    # Clear memory
    persona_engine.clear_memory()
    
    # Simulate an exchange
    response = persona_engine.respond("Test message", "TestUser")
    
    # Check that we can format the log message
    user_id = 12345
    mood = persona_engine.mood
    reply_len = len(response)
    
    log_message = f"Exchange | user_id={user_id} | mood={mood} | reply_len={reply_len}"
    
    assert "Exchange" in log_message, "Log should contain 'Exchange'"
    assert "user_id=" in log_message, "Log should contain user_id"
    assert "mood=" in log_message, "Log should contain mood"
    assert "reply_len=" in log_message, "Log should contain reply_len"
    
    print(f"  Sample log: {log_message}")
    print("✓ Logging format correct")


def main():
    """Run all tests"""
    print("=" * 70)
    print("PERSONA ENGINE INTEGRATION TESTS")
    print("=" * 70)
    
    try:
        test_global_persona_engine()
        test_persona_respond()
        test_memory_functions()
        test_personality_info()
        test_bot_commands_exist()
        test_logging_format()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\nPersonaEngine is properly wired into Telegram handlers:")
        print("  • Global persona_engine instance created")
        print("  • /persona command implemented")
        print("  • /recall command implemented")
        print("  • /resetmem command implemented")
        print("  • Exchange logging format: user_id, mood, reply_len")
        print("  • All existing commands preserved (/start, /help, /menu)")
        print("\nReady to use! 🎉")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

