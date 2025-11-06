#!/usr/bin/env python3
"""
Test script for Ollama integration with Luna Noir bot
"""

import sys
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def test_ollama_client():
    """Test basic Ollama client functionality"""
    print("\n" + "="*60)
    print("TEST 1: Ollama Client")
    print("="*60)

    try:
        from src.dialogue.ollama_client import create_ollama_client

        # Use mistral:latest which is available
        client = create_ollama_client(model="mistral:latest")
        print(f"✓ Ollama client created")
        
        # Check if server is running
        if client.is_available():
            print(f"✓ Ollama server is running at {client.base_url}")
            
            # List models
            models = client.list_models()
            if models:
                print(f"✓ Available models: {', '.join(models)}")
            else:
                print("⚠ No models found. Run: ollama pull llama3.1:8b")
                return False
            
            # Test generation
            print("\nTesting response generation...")
            response = client.generate(
                prompt="Say hi in one sentence.",
                system_prompt="You are Luna Noir, a witty AI companion."
            )
            
            if response:
                print(f"✓ Response generated: {response}")
                return True
            else:
                print("✗ Failed to generate response")
                return False
        else:
            print("✗ Ollama server is not running")
            print("  Start it with: ollama serve")
            print("  Then pull a model: ollama pull llama3.1:8b")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_persona_engine():
    """Test PersonaEngine with Ollama integration"""
    print("\n" + "="*60)
    print("TEST 2: PersonaEngine with Ollama")
    print("="*60)

    try:
        # Set environment variable for model
        os.environ['OLLAMA_MODEL'] = 'mistral:latest'

        from src.dialogue.persona_engine import PersonaEngine

        # Create persona with Ollama enabled
        persona = PersonaEngine(use_ollama=True)
        print(f"✓ PersonaEngine created: {persona.name} {persona.version}")
        print(f"  Ollama enabled: {persona.use_ollama}")
        
        # Test different moods
        test_cases = [
            ("Hey Luna, I miss you so much", "affectionate"),
            ("Why do you always do this?", "curious"),
            ("I'm feeling really down today", "comforting"),
            ("Haha that's hilarious!", "playful"),
            ("What's your favorite color?", "curious")
        ]
        
        print("\nTesting mood detection and responses:")
        for message, expected_mood in test_cases:
            print(f"\n  User: {message}")
            response = persona.respond(message, "Alex")
            print(f"  Luna ({persona.mood}): {response}")
            
            if persona.mood == expected_mood:
                print(f"  ✓ Mood correctly detected: {expected_mood}")
            else:
                print(f"  ⚠ Mood mismatch: expected {expected_mood}, got {persona.mood}")
        
        # Test memory
        print("\n" + "-"*60)
        print("Memory Summary:")
        print(persona.get_memory_summary())
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_fallback_mode():
    """Test PersonaEngine fallback mode (without Ollama)"""
    print("\n" + "="*60)
    print("TEST 3: PersonaEngine Fallback Mode")
    print("="*60)
    
    try:
        from src.dialogue.persona_engine import PersonaEngine
        
        # Create persona with Ollama disabled
        persona = PersonaEngine(use_ollama=False)
        print(f"✓ PersonaEngine created in fallback mode")
        print(f"  Ollama enabled: {persona.use_ollama}")
        
        # Test response
        response = persona.respond("Hey Luna!", "TestUser")
        print(f"\n  User: Hey Luna!")
        print(f"  Luna: {response}")
        print(f"✓ Fallback responses working")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("LUNA NOIR - OLLAMA INTEGRATION TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test 1: Ollama Client
    results.append(("Ollama Client", test_ollama_client()))
    
    # Test 2: PersonaEngine with Ollama
    results.append(("PersonaEngine with Ollama", test_persona_engine()))
    
    # Test 3: Fallback mode
    results.append(("Fallback Mode", test_fallback_mode()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed!")
        print("\nNext steps:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Update your .env file with Ollama settings")
        print("3. Start your bot and test it!")
    else:
        print("\n⚠ Some tests failed. Check the output above.")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is installed: brew install ollama")
        print("2. Start Ollama server: ollama serve")
        print("3. Pull a model: ollama pull llama3.1:8b")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

