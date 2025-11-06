# Ollama Integration Setup Guide

Luna Noir now supports **local AI** using Ollama! This means you can run the bot with powerful language models on your own machine without needing API keys or cloud services.

## 🚀 Quick Setup

### 1. Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download
```

### 2. Start Ollama Server

```bash
ollama serve
```

Keep this running in a separate terminal window.

### 3. Pull a Model

```bash
# Recommended: Llama 3.1 8B (fast, good quality)
ollama pull llama3.1:8b

# Alternative models:
ollama pull llama3.1:70b    # Better quality, slower
ollama pull mistral:7b      # Faster, smaller
ollama pull phi3:mini       # Very fast, lightweight
```

### 4. Configure Environment

Update your `.env` file:

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_TEMPERATURE=0.8
```

### 5. Test the Integration

```bash
python test_ollama_integration.py
```

You should see:
```
✓ PASSED: Ollama Client
✓ PASSED: PersonaEngine with Ollama
✓ PASSED: Fallback Mode
🎉 All tests passed!
```

## 🎯 How It Works

### Architecture

```
User Message
    ↓
PersonaEngine (Mood Detection)
    ↓
Ollama Client (AI Generation)
    ↓
Luna's Response
```

### Features

1. **Mood Detection**: Analyzes user messages for emotional tone
2. **Context-Aware**: Uses conversation history for better responses
3. **Personality System**: Maintains Luna's unique character
4. **Graceful Fallback**: Uses template responses if Ollama is unavailable

### Example Flow

```python
from src.dialogue.persona_engine import PersonaEngine

# Create persona with Ollama enabled
luna = PersonaEngine(use_ollama=True)

# Generate response
response = luna.respond("I miss you", "Alex")
# Luna detects "affectionate" mood and generates warm response
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3.1:8b` | Model to use |
| `OLLAMA_TEMPERATURE` | `0.8` | Response creativity (0.0-1.0) |

### Model Recommendations

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| `llama3.1:8b` | ~4.7GB | Fast | Good | **Recommended** |
| `llama3.1:70b` | ~40GB | Slow | Excellent | High-end systems |
| `mistral:7b` | ~4.1GB | Very Fast | Good | Quick responses |
| `phi3:mini` | ~2.3GB | Ultra Fast | Decent | Low-resource systems |

## 🧪 Testing

### Test Ollama Client Only

```python
from src.dialogue.ollama_client import create_ollama_client

client = create_ollama_client()

if client.is_available():
    response = client.generate(
        prompt="Say hi!",
        system_prompt="You are Luna Noir, a witty AI companion."
    )
    print(response)
```

### Test Full PersonaEngine

```python
from src.dialogue.persona_engine import PersonaEngine

luna = PersonaEngine(use_ollama=True)

# Test different moods
print(luna.respond("I love you", "Alex"))  # affectionate
print(luna.respond("Why?", "Alex"))        # curious
print(luna.respond("I'm sad", "Alex"))     # comforting
```

### Run Test Suite

```bash
python test_ollama_integration.py
```

## 🐛 Troubleshooting

### Ollama Server Not Running

**Error**: `Connection refused` or `Ollama server not available`

**Solution**:
```bash
# Start Ollama in a separate terminal
ollama serve
```

### Model Not Found

**Error**: `model 'llama3.1:8b' not found`

**Solution**:
```bash
# Pull the model
ollama pull llama3.1:8b

# List available models
ollama list
```

### Slow Responses

**Solutions**:
1. Use a smaller model: `ollama pull phi3:mini`
2. Reduce `OLLAMA_TEMPERATURE` to 0.5
3. Decrease max_tokens in `ollama_client.py`

### Fallback Mode Activated

If you see "Falling back to template responses", it means:
- Ollama server isn't running, OR
- The model isn't available

The bot will still work using pre-defined responses.

## 📊 Performance

### Response Times (approximate)

| Model | First Response | Subsequent |
|-------|---------------|------------|
| `llama3.1:8b` | 2-5s | 1-3s |
| `mistral:7b` | 1-3s | 0.5-2s |
| `phi3:mini` | 0.5-2s | 0.3-1s |

*Times vary based on hardware (CPU/GPU)*

## 🔄 Switching Between Ollama and OpenAI

### Use Ollama (Local)

```python
luna = PersonaEngine(use_ollama=True)
```

### Use Templates (No AI)

```python
luna = PersonaEngine(use_ollama=False)
```

### Future: OpenAI Support

To add OpenAI support later, you can modify `persona_engine.py` to check for OpenAI API key and use it as an alternative to Ollama.

## 🎨 Customization

### Change Model

```bash
# In .env
OLLAMA_MODEL=mistral:7b
```

### Adjust Creativity

```bash
# In .env
OLLAMA_TEMPERATURE=0.9  # More creative
OLLAMA_TEMPERATURE=0.5  # More focused
```

### Modify System Prompt

Edit `_build_system_prompt()` in `src/dialogue/persona_engine.py` to change Luna's personality instructions.

## 📚 Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Available Models](https://ollama.com/library)
- [Model Comparison](https://ollama.com/blog/model-comparison)

## ✅ Next Steps

1. ✅ Install Ollama
2. ✅ Start server (`ollama serve`)
3. ✅ Pull model (`ollama pull llama3.1:8b`)
4. ✅ Run tests (`python test_ollama_integration.py`)
5. 🚀 Start your bot and enjoy AI-powered conversations!

---

**Need help?** Check the troubleshooting section or open an issue on GitHub.

