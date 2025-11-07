"""
ElevenLabs Text-to-Speech Module
Synthesizes audio from text using ElevenLabs API.
"""

import os
import requests
import logging

logger = logging.getLogger(__name__)

# ElevenLabs API Configuration
ELEVEN_API = "https://api.elevenlabs.io/v1/text-to-speech"
API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "Rachel")


def synthesize_tts(text: str, voice_id: str = None) -> bytes:
    """
    Synthesize text to speech using ElevenLabs API.
    
    Args:
        text: Text to synthesize (max 1000 chars for latency)
        voice_id: ElevenLabs voice ID (default: from env or "Rachel")
        
    Returns:
        bytes: MP3 audio data
        
    Raises:
        RuntimeError: If ELEVENLABS_API_KEY is not set
        requests.HTTPError: If API request fails
    """
    if not API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY missing in .env file")
    
    v = voice_id or VOICE_ID
    url = f"{ELEVEN_API}/{v}"
    
    headers = {
        "xi-api-key": API_KEY,
        "accept": "audio/mpeg",
        "content-type": "application/json"
    }
    
    payload = {
        "text": text[:1000],  # Keep it short for latency
        "voice_settings": {
            "stability": 0.55,           # Lower = more natural variation (less robotic)
            "similarity_boost": 0.75,    # Balanced for natural sound
            "style": 0.65,               # Higher style = more expressive, less robotic
            "use_speaker_boost": True    # Enhance voice clarity
        },
        "model_id": "eleven_turbo_v2_5"  # Newest model - more natural sounding
    }
    
    logger.info(f"Synthesizing TTS for {len(text)} chars with voice {v}")
    
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        logger.info(f"TTS synthesis successful, {len(r.content)} bytes")
        return r.content
    except requests.exceptions.RequestException as e:
        logger.error(f"TTS synthesis failed: {e}")
        raise

