#!/usr/bin/env python3
"""
LLM Client for Open-Source Models
Supports Ollama, LM Studio, text-generation-webui, and any OpenAI-compatible endpoint
"""
import os
import requests
import logging

logger = logging.getLogger(__name__)

BASE = os.getenv("LLM_API_BASE", "http://localhost:11434/v1")
MODEL = os.getenv("LLM_MODEL", "llama3:8b")
API_KEY = os.getenv("LLM_API_KEY", "none")


def query_llm(prompt: str, max_tokens: int = 512, system_prompt: str = None) -> str:
    """
    Query an open-source LLM endpoint (Ollama, LM Studio, etc.)
    
    Args:
        prompt: User message/prompt
        max_tokens: Maximum tokens to generate
        system_prompt: Optional system prompt for context
    
    Returns:
        Generated text response
    """
    headers = {"Content-Type": "application/json"}
    
    # Add API key if provided (for authenticated endpoints)
    if API_KEY not in ("", "none", None):
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    # Build messages array
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    # Request body - BALANCED FOR QUALITY & SPEED
    body = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": min(max_tokens, 400),  # Increased for more thoughtful responses
        "temperature": 0.85,  # Slightly higher for more creative responses
        "stream": False,
        "top_p": 0.92  # Balanced sampling for quality
    }

    try:
        logger.info(f"Querying LLM at {BASE} with model {MODEL}")
        # Balanced timeout for thoughtful responses
        r = requests.post(
            f"{BASE}/chat/completions",
            json=body,
            headers=headers,
            timeout=30  # Increased for longer, better responses
        )
        r.raise_for_status()
        data = r.json()

        # Extract response
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")

        if not content:
            logger.warning(f"Empty response from LLM: {data}")
            return "I'm having trouble thinking right now. Try again?"

        logger.info(f"LLM response received ({len(content)} chars)")
        return content

    except requests.exceptions.Timeout:
        logger.error("LLM request timed out")
        return "I'm thinking too slowly right now. Try again in a moment?"
    
    except requests.exceptions.ConnectionError:
        logger.error(f"Cannot connect to LLM at {BASE}")
        return "I can't reach my brain right now. Is the LLM server running?"
    
    except requests.exceptions.HTTPError as e:
        logger.error(f"LLM HTTP error: {e}")
        return "Something went wrong with my thinking process."
    
    except Exception as e:
        logger.exception(f"Unexpected LLM error: {e}")
        return "I'm having trouble thinking right now."


def get_model_info() -> dict:
    """Get current LLM configuration"""
    return {
        "provider": os.getenv("MODEL_PROVIDER", "open_llm"),
        "base_url": BASE,
        "model": MODEL,
        "has_api_key": API_KEY not in ("", "none", None)
    }

