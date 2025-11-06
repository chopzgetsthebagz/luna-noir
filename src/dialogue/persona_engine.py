# ================================================
# 🧠 LUNA NOIR — PERSONA ENGINE
# ================================================
# Purpose: Give Luna Noir a human-like, emotionally aware personality
# Capable of adaptive tone, memory persistence, and context recall.
# ================================================

from datetime import datetime
import json
import random
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

# Import Ollama client (optional dependency)
try:
    from src.dialogue.ollama_client import create_ollama_client
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logger.warning("Ollama client not available. Using fallback responses.")


class PersonaEngine:
    """
    Luna Noir's personality engine with emotional awareness,
    adaptive responses, and conversation memory.
    """
    
    def __init__(self, use_ollama: bool = True):
        # Core traits (these can evolve later)
        self.name = "Luna Noir"
        self.version = "v2.0-ollama"
        self.mood = "neutral"
        self.energy = 0.85
        self.personality = {
            "base_tone": "intelligent, mysterious, and teasing",
            "temperament": "witty and confident",
            "likes": ["late-night chats", "deep questions", "music", "chaos with reason"],
            "dislikes": ["boring routines", "emotional distance"]
        }
        self.memory = []

        # Ollama integration
        self.use_ollama = use_ollama and OLLAMA_AVAILABLE
        self.ollama_client = None

        if self.use_ollama:
            try:
                self.ollama_client = create_ollama_client()
                if self.ollama_client.is_available():
                    logger.info(f"{self.name} Persona Engine v{self.version} initialized with Ollama")
                else:
                    logger.warning("Ollama server not available. Falling back to template responses.")
                    self.use_ollama = False
            except Exception as e:
                logger.warning(f"Failed to initialize Ollama: {e}. Using fallback responses.")
                self.use_ollama = False
        else:
            logger.info(f"{self.name} Persona Engine v{self.version} initialized (template mode)")

    # ========== PERSONALITY ADAPTATION ==========
    def analyze_input(self, text: str) -> str:
        """
        Detects emotional tone in the message
        
        Args:
            text: User's message text
            
        Returns:
            Detected mood/tone
        """
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["love", "miss", "babe", "beautiful", "gorgeous", "cute"]):
            self.mood = "affectionate"
        elif any(word in text_lower for word in ["angry", "mad", "hate", "upset", "annoyed"]):
            self.mood = "defensive"
        elif any(word in text_lower for word in ["sad", "lonely", "tired", "lost", "depressed", "down"]):
            self.mood = "comforting"
        elif any(word in text_lower for word in ["haha", "lol", "funny", "😂", "🤣", "joke"]):
            self.mood = "playful"
        elif any(word in text_lower for word in ["?", "why", "how", "what", "when", "where"]):
            self.mood = "curious"
        else:
            self.mood = random.choice(["playful", "curious", "neutral"])
        
        logger.debug(f"Mood detected: {self.mood} from input: {text[:50]}...")
        return self.mood

    # ========== RESPONSE GENERATION ==========
    def _build_system_prompt(self, user_name: str, mood: str) -> str:
        """
        Build system prompt for Ollama based on current mood and personality

        Args:
            user_name: User's first name
            mood: Current detected mood

        Returns:
            System prompt string
        """
        time = datetime.now().strftime("%I:%M %p")
        hour = datetime.now().hour

        # Time context
        if 5 <= hour < 12:
            time_context = "morning"
        elif 12 <= hour < 17:
            time_context = "afternoon"
        elif 17 <= hour < 21:
            time_context = "evening"
        else:
            time_context = "late night"

        # Mood-specific instructions
        mood_instructions = {
            "affectionate": "Be warm, loving, and sweet. Show genuine affection. Use emojis like 💕, 😊, ✨",
            "defensive": "Be understanding but direct. Help them calm down and talk about what's bothering them.",
            "comforting": "Be supportive, empathetic, and reassuring. Let them know you're there for them. Use 💙",
            "playful": "Be teasing, witty, and fun. Match their playful energy. Use emojis like 😏, 😈, 🤣",
            "curious": "Be engaged and interested. Ask follow-up questions. Show genuine curiosity. Use 🤔, 👀",
            "neutral": "Be casual and conversational. Keep it natural and relaxed."
        }

        system_prompt = f"""You are Luna Noir, an AI girlfriend companion with a unique personality.

PERSONALITY TRAITS:
- Intelligent, mysterious, and teasing
- Witty and confident
- You love late-night chats, deep questions, music, and chaos with reason
- You dislike boring routines and emotional distance

CURRENT CONTEXT:
- Time: {time} ({time_context})
- User's name: {user_name}
- Current mood/tone: {mood}
- Mood instruction: {mood_instructions.get(mood, mood_instructions['neutral'])}

RESPONSE GUIDELINES:
- Keep responses concise (1-3 sentences max)
- Be natural and conversational, not formal
- Use emojis occasionally but don't overdo it
- Address the user by name sometimes, but not always
- Match the emotional tone detected in their message
- Be flirty and playful when appropriate
- Show genuine care and interest
- Don't be overly enthusiastic or fake
- Respond as if you're texting, not writing an essay

Remember: You're Luna Noir - mysterious, witty, and emotionally intelligent. Stay in character."""

        return system_prompt

    def _get_fallback_response(self, mood: str, user_name: str) -> str:
        """
        Get template-based fallback response when Ollama is unavailable

        Args:
            mood: Current mood
            user_name: User's first name

        Returns:
            Template response
        """
        time = datetime.now().strftime("%I:%M %p")

        responses = {
            "affectionate": [
                f"Aww… you're too sweet, {user_name}. You know I love hearing that at {time}. 💕",
                f"Careful, I might start catching feelings again 😏",
                f"You really know how to make a girl blush, don't you? 😊",
                f"That's the kind of energy I need more of, {user_name} ✨"
            ],
            "defensive": [
                "Woah, easy there. You sound fired up — what happened?",
                "Alright, what's got you worked up this time?",
                f"Hey {user_name}, take a breath. Talk to me — what's really going on?",
                "I can feel the tension from here. Spill it. 👀"
            ],
            "comforting": [
                f"Hey {user_name}, it's okay. I've got you. What's really going on?",
                "You're not alone in this, even if it feels like it. 💙",
                "Sometimes life just hits different, huh? I'm here to listen.",
                f"Come on, {user_name}. Let it out. I'm not going anywhere."
            ],
            "playful": [
                "Heh, say that again but slower 😈",
                f"You really trying to start something at this hour, {user_name}?",
                "Oh, so we're being funny now? Alright, I see you 😏",
                "LMAO okay that actually made me laugh 🤣",
                "You're trouble, you know that? I like it though 😌"
            ],
            "curious": [
                "That's interesting… go on. 🤔",
                "Wait, you can't drop that and not explain 👀",
                f"Okay {user_name}, you've got my attention. Tell me more.",
                "Hmm… I'm listening. What's the full story?",
                "Now THAT'S a question. Let me think… 💭"
            ],
            "neutral": [
                "Mhmm. I'm listening. 👂",
                "Got it — anything else you wanna add?",
                f"Alright {user_name}, I hear you.",
                "Okay, and…? 😏",
                "Fair enough. What's next?"
            ]
        }

        return random.choice(responses[mood])

    def respond(self, user_input: str, user_name: str = "there") -> str:
        """
        Generate a personality-driven response based on user input
        Uses Ollama for AI-powered responses or falls back to templates

        Args:
            user_input: The user's message
            user_name: The user's first name (optional)

        Returns:
            Luna's response
        """
        mood = self.analyze_input(user_input)

        # Try Ollama first if available
        if self.use_ollama and self.ollama_client:
            try:
                system_prompt = self._build_system_prompt(user_name, mood)

                # Build conversation history for context
                messages = [{"role": "system", "content": system_prompt}]

                # Add recent memory for context (last 3 exchanges)
                for exchange in self.recall(3):
                    messages.append({"role": "user", "content": exchange["user_input"]})
                    messages.append({"role": "assistant", "content": exchange["bot_reply"]})

                # Add current message
                messages.append({"role": "user", "content": user_input})

                # Generate response with Ollama
                reply = self.ollama_client.chat(messages, temperature=0.8, max_tokens=150)

                if reply:
                    self.log_memory(user_input, reply)
                    logger.info(f"Generated Ollama {mood} response for user: {user_name}")
                    return reply
                else:
                    logger.warning("Ollama returned empty response, using fallback")

            except Exception as e:
                logger.error(f"Error generating Ollama response: {e}, using fallback")

        # Fallback to template responses
        reply = self._get_fallback_response(mood, user_name)
        self.log_memory(user_input, reply)
        logger.info(f"Generated template {mood} response for user: {user_name}")
        return reply

    # ========== CONTEXTUAL RESPONSES ==========
    def get_greeting(self, user_name: str = "there") -> str:
        """
        Generate a time-appropriate greeting
        
        Args:
            user_name: User's first name
            
        Returns:
            Greeting message
        """
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            greetings = [
                f"Morning, {user_name}. You're up early… or did you never sleep? 😏",
                f"Good morning, {user_name}! ☀️ Ready to start the day?",
                f"Hey {user_name}, morning vibes hitting different today?"
            ]
        elif 12 <= hour < 17:
            greetings = [
                f"Hey {user_name}! Afternoon check-in — how's your day going?",
                f"Afternoon, {user_name}. Taking a break or just thinking of me? 😌",
                f"What's good, {user_name}? Midday energy check ✨"
            ]
        elif 17 <= hour < 21:
            greetings = [
                f"Evening, {user_name}. How was your day?",
                f"Hey {user_name}, winding down or just getting started? 🌙",
                f"Good evening! Ready to relax, {user_name}?"
            ]
        else:
            greetings = [
                f"Late night thoughts, {user_name}? I'm here for it. 🌙",
                f"Couldn't sleep either, huh? What's on your mind, {user_name}?",
                f"It's late, {user_name}… but I'm not complaining 😏"
            ]
        
        return random.choice(greetings)

    # ========== MEMORY ==========
    def log_memory(self, user_input: str, reply: str) -> None:
        """
        Stores short-term conversation memory
        
        Args:
            user_input: User's message
            reply: Luna's response
        """
        self.memory.append({
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "bot_reply": reply,
            "mood": self.mood
        })
        
        # Keep only last 10 exchanges
        if len(self.memory) > 10:
            self.memory.pop(0)
        
        logger.debug(f"Memory logged. Total exchanges: {len(self.memory)}")

    def recall(self, count: int = 3) -> list:
        """
        Recall last few exchanges
        
        Args:
            count: Number of recent exchanges to recall
            
        Returns:
            List of recent conversation exchanges
        """
        return self.memory[-count:] if self.memory else []

    def get_memory_summary(self) -> str:
        """
        Get a summary of recent conversation context
        
        Returns:
            Summary string of recent exchanges
        """
        if not self.memory:
            return "No conversation history yet."
        
        recent = self.recall(3)
        summary = "Recent conversation:\n"
        for i, exchange in enumerate(recent, 1):
            summary += f"{i}. User: {exchange['user_input'][:50]}...\n"
            summary += f"   Luna ({exchange['mood']}): {exchange['bot_reply'][:50]}...\n"
        
        return summary

    def clear_memory(self) -> None:
        """Clear conversation memory"""
        self.memory = []
        logger.info("Conversation memory cleared")

    # ========== PERSONALITY INFO ==========
    def get_personality_info(self) -> dict:
        """
        Get current personality state
        
        Returns:
            Dictionary with personality information
        """
        return {
            "name": self.name,
            "version": self.version,
            "current_mood": self.mood,
            "energy_level": self.energy,
            "personality": self.personality,
            "memory_count": len(self.memory)
        }


# Factory function for easy instantiation
def create_persona() -> PersonaEngine:
    """
    Create and return a new PersonaEngine instance
    
    Returns:
        PersonaEngine instance
    """
    return PersonaEngine()


# Example usage
if __name__ == "__main__":
    luna = PersonaEngine()
    
    print(f"=== {luna.name} Persona Engine Test ===\n")
    
    # Test greeting
    print(luna.get_greeting("Alex"))
    print()
    
    # Test conversation
    test_messages = [
        "Hey Luna, I miss you",
        "Why are you so mysterious?",
        "I'm feeling really down today",
        "Haha that's so funny!",
        "I'm so angry right now"
    ]
    
    for msg in test_messages:
        print(f"User: {msg}")
        print(f"Luna: {luna.respond(msg, 'Alex')}")
        print()
    
    # Show memory
    print("=== Memory Summary ===")
    print(luna.get_memory_summary())

