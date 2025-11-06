# Luna Noir Persona Engine - Developer Guide

## Overview

The Persona Engine gives Luna Noir an adaptive, emotionally-aware personality that responds naturally to user messages. It's designed to make conversations feel authentic and engaging.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Telegram User Message                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              src/core/bot.py (LunaNoirBot)                   │
│  • Receives message via webhook                              │
│  • Calls self.persona.respond(message, user_name)            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           src/dialogue/persona.py (PersonaEngine)            │
│  1. analyze_input() - Detects mood from keywords             │
│  2. respond() - Generates mood-appropriate response          │
│  3. log_memory() - Stores exchange in memory                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Response sent to user                      │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. PersonaEngine Class

**Location:** `src/dialogue/persona.py`

**Key Attributes:**
- `name`: "Luna Noir"
- `version`: "v1.0"
- `mood`: Current emotional state (affectionate, playful, comforting, etc.)
- `energy`: Energy level (0.0-1.0)
- `personality`: Dict of personality traits
- `memory`: List of recent conversation exchanges

**Key Methods:**

#### `analyze_input(text: str) -> str`
Detects emotional tone in user's message using keyword matching.

**Returns:** Detected mood (affectionate, defensive, comforting, playful, curious, neutral)

**Example:**
```python
mood = persona.analyze_input("I miss you so much")
# Returns: "affectionate"
```

#### `respond(user_input: str, user_name: str = "there") -> str`
Generates a personality-driven response based on detected mood.

**Parameters:**
- `user_input`: The user's message
- `user_name`: User's first name (optional)

**Returns:** Luna's response string

**Example:**
```python
response = persona.respond("I'm feeling sad", "Alex")
# Returns: "Hey Alex, it's okay. I've got you. What's really going on?"
```

#### `get_greeting(user_name: str = "there") -> str`
Generates time-appropriate greeting.

**Time Ranges:**
- 5am-12pm: Morning greetings
- 12pm-5pm: Afternoon greetings
- 5pm-9pm: Evening greetings
- 9pm-5am: Late night greetings

**Example:**
```python
greeting = persona.get_greeting("Alex")
# At 11pm: "Late night thoughts, Alex? I'm here for it. 🌙"
```

#### `log_memory(user_input: str, reply: str) -> None`
Stores conversation exchange in memory (max 10 exchanges).

#### `recall(count: int = 3) -> list`
Retrieves recent conversation exchanges.

**Example:**
```python
recent = persona.recall(3)
# Returns last 3 exchanges with timestamps and moods
```

#### `get_personality_info() -> dict`
Returns current personality state including mood, energy, traits, and memory count.

### 2. Bot Integration

**Location:** `src/core/bot.py`

The PersonaEngine is integrated into the LunaNoirBot class:

```python
class LunaNoirBot:
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(token=token)
        self.persona = PersonaEngine()  # ← Persona integration
```

**Message Handler:**
```python
async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text
    
    # Generate personality-driven response
    response = self.persona.respond(message_text, user.first_name)
    
    await update.message.reply_text(response)
```

## Mood Detection

### Keyword Mapping

| Mood | Keywords | Response Style |
|------|----------|----------------|
| **Affectionate** | love, miss, babe, beautiful, gorgeous, cute | Warm, loving, sweet |
| **Defensive** | angry, mad, hate, upset, annoyed | Calm, understanding, de-escalating |
| **Comforting** | sad, lonely, tired, lost, depressed, down | Supportive, empathetic, caring |
| **Playful** | haha, lol, funny, 😂, 🤣, joke | Teasing, fun, energetic |
| **Curious** | ?, why, how, what, when, where | Engaged, thoughtful, interested |
| **Neutral** | (default) | Conversational, balanced |

### Adding New Moods

To add a new mood:

1. **Update `analyze_input()` in `persona.py`:**
```python
elif any(word in text_lower for word in ["excited", "amazing", "awesome"]):
    self.mood = "enthusiastic"
```

2. **Add response pool in `respond()` method:**
```python
responses = {
    # ... existing moods ...
    "enthusiastic": [
        "YES! That energy! I love it! 🔥",
        "Now THAT'S what I'm talking about! ✨",
        "Your excitement is contagious! Tell me more!"
    ]
}
```

## Memory System

### How It Works

1. Every exchange is logged with:
   - Timestamp (ISO format)
   - User input
   - Bot reply
   - Detected mood

2. Memory is stored in `self.memory` list (max 10 items)

3. Oldest exchanges are removed when limit is reached

### Memory Structure

```python
{
    "timestamp": "2025-10-29T21:30:45.123456",
    "user_input": "I miss you",
    "bot_reply": "Aww… you're too sweet...",
    "mood": "affectionate"
}
```

### Accessing Memory

```python
# Get last 3 exchanges
recent = persona.recall(3)

# Get formatted summary
summary = persona.get_memory_summary()

# Clear memory
persona.clear_memory()
```

## Bot Commands

### Existing Commands

| Command | Description | Handler Method |
|---------|-------------|----------------|
| `/start` | Personalized greeting | `start_command()` |
| `/menu` | Feature menu | `menu_command()` |
| `/help` | Help information | `help_command()` |
| `/mood` | Show personality state | `mood_command()` |
| `/memory` | Show conversation history | `memory_command()` |

### Adding New Commands

1. **Create handler method in `bot.py`:**
```python
async def custom_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # Your logic here
    await update.message.reply_text("Response")
```

2. **Register in `setup_handlers()`:**
```python
application.add_handler(CommandHandler("custom", self.custom_command))
```

3. **Update `/menu` to include new command**

## Testing

### Run All Tests
```bash
python test_bot_structure.py
```

### Test Persona Directly
```python
from src.dialogue.persona import PersonaEngine

persona = PersonaEngine()
response = persona.respond("I love you", "Alex")
print(response)
```

### Interactive Demo
```bash
python demo_persona.py
```

## Future Enhancements

### Planned Features

1. **OpenAI GPT Integration**
   - Use persona mood as context for GPT prompts
   - Generate more sophisticated responses
   - Maintain personality consistency

2. **Database Persistence**
   - Store long-term memory in SQLite/PostgreSQL
   - User-specific personality profiles
   - Conversation history across sessions

3. **Advanced Sentiment Analysis**
   - Use NLP libraries (NLTK, spaCy) for better mood detection
   - Detect sarcasm, irony, complex emotions
   - Multi-language support

4. **Personality Evolution**
   - Adapt personality based on user interactions
   - Learn user preferences over time
   - Dynamic trait adjustment

5. **Voice Integration**
   - ElevenLabs voice synthesis with mood-appropriate tone
   - Voice message responses
   - Emotion in voice delivery

## Best Practices

### Do's ✅

- Keep response pools diverse and natural
- Log important state changes
- Test mood detection with edge cases
- Maintain personality consistency
- Use user's name for personalization

### Don'ts ❌

- Don't make responses too long
- Don't use offensive or inappropriate language
- Don't store sensitive user data in memory
- Don't hardcode user-specific information
- Don't ignore error handling

## Troubleshooting

### Mood Not Detecting Correctly

**Problem:** Messages not triggering expected mood

**Solution:** 
- Check keyword list in `analyze_input()`
- Add more keywords for that mood
- Test with `demo_persona.py`

### Memory Not Persisting

**Problem:** Memory clears between bot restarts

**Solution:**
- This is expected behavior (in-memory only)
- Implement database persistence for long-term storage
- Use `/memory` command to verify current session memory

### Responses Feel Repetitive

**Problem:** Same responses appearing too often

**Solution:**
- Add more response variations to each mood pool
- Implement response history tracking
- Use randomization with weights

## Contributing

When adding new features to the Persona Engine:

1. Update `persona.py` with new methods
2. Add tests to `test_bot_structure.py`
3. Update this guide with documentation
4. Add examples to `demo_persona.py`
5. Update README.md if user-facing

## Resources

- **Main Code:** `src/dialogue/persona.py`
- **Bot Integration:** `src/core/bot.py`
- **Tests:** `test_bot_structure.py`
- **Demo:** `demo_persona.py`
- **Documentation:** `README.md`, `QUICKSTART.md`

---

**Version:** 1.0  
**Last Updated:** October 29, 2025  
**Author:** Luna Noir Development Team

