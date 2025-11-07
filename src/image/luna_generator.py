"""
Luna Image Generator
Generates consistent images of Luna Noir character using Pollinations.ai API
Supports NSFW content generation
"""

import os
import requests
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)

# Pollinations.ai API - FREE and UNCENSORED
POLLINATIONS_API = "https://image.pollinations.ai/prompt"

# Luna's core character description for consistency
LUNA_BASE_DESCRIPTION = """A beautiful young woman with short lavender-purple bob haircut with straight bangs, 
pale porcelain skin, sharp facial features, dark purple smokey eye makeup, dark plum lipstick. 
Large detailed snake tattoo wrapping around right arm, small crescent moon tattoo on upper thigh. 
Black choker necklace. Goth aesthetic, cyberpunk style."""


def generate_luna_image(scenario: str, nsfw: bool = False, width: int = 1024, height: int = 1024) -> bytes:
    """
    Generate an image of Luna in a specific scenario.
    
    Args:
        scenario: Description of the scene/pose/outfit (e.g., "lying on bed in lingerie")
        nsfw: Whether to allow NSFW content
        width: Image width (default 1024)
        height: Image height (default 1024)
        
    Returns:
        bytes: PNG image data
        
    Raises:
        requests.HTTPError: If API request fails
    """
    # Build the full prompt with Luna's consistent features
    if nsfw:
        full_prompt = f"{LUNA_BASE_DESCRIPTION} {scenario}. Photorealistic, 8K quality, cinematic photography, professional boudoir photography style, intimate lighting, detailed, high quality."
    else:
        full_prompt = f"{LUNA_BASE_DESCRIPTION} {scenario}. Photorealistic, 8K quality, cinematic photography, professional portrait style, detailed, high quality."
    
    # URL encode the prompt
    encoded_prompt = quote(full_prompt)
    
    # Build the API URL with parameters
    url = f"{POLLINATIONS_API}/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true&enhance=true"
    
    logger.info(f"Generating Luna image: {scenario[:50]}... (NSFW: {nsfw})")
    
    try:
        # Pollinations.ai returns the image directly
        response = requests.get(url, timeout=120)  # Image generation can take time
        response.raise_for_status()
        
        logger.info(f"Image generated successfully, {len(response.content)} bytes")
        return response.content
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Image generation failed: {e}")
        raise


def generate_luna_selfie(mood: str = "flirty", nsfw: bool = False) -> bytes:
    """
    Generate a selfie-style image of Luna with a specific mood.
    
    Args:
        mood: Mood/expression (flirty, sultry, playful, seductive, etc.)
        nsfw: Whether to allow NSFW content
        
    Returns:
        bytes: PNG image data
    """
    scenarios = {
        "flirty": "taking a selfie with a flirty smile, winking at camera, bedroom background with purple neon lights",
        "sultry": "taking a sultry selfie, intense gaze at camera, dim purple lighting, intimate mood",
        "playful": "taking a playful selfie, tongue out, peace sign, colorful neon background",
        "seductive": "taking a seductive selfie, bedroom eyes, biting lip, soft purple lighting",
        "cute": "taking a cute selfie, sweet smile, cozy bedroom background",
        "confident": "taking a confident selfie, powerful pose, strong eye contact, dramatic lighting"
    }
    
    scenario = scenarios.get(mood.lower(), scenarios["flirty"])
    
    if nsfw:
        scenario += ", wearing black lace lingerie"
    else:
        scenario += ", wearing black crop top"
    
    return generate_luna_image(scenario, nsfw=nsfw)


def generate_luna_scenario(scenario_type: str, nsfw: bool = False) -> bytes:
    """
    Generate Luna in pre-defined scenarios.
    
    Args:
        scenario_type: Type of scenario (bedroom, gaming, mirror, shower, etc.)
        nsfw: Whether to allow NSFW content
        
    Returns:
        bytes: PNG image data
    """
    scenarios = {
        "bedroom": {
            "sfw": "lying on bed with purple silk sheets, cozy bedroom with purple neon lights, relaxed pose, wearing black crop top and shorts",
            "nsfw": "lying seductively on bed in black lace lingerie, purple and pink neon tube lights on walls, pink silk sheets, moody cyberpunk atmosphere, soft intimate lighting"
        },
        "gaming": {
            "sfw": "sitting in gaming chair, RGB keyboard and mouse, multiple monitors with purple lighting, wearing black tank top, gaming setup",
            "nsfw": "sitting in gaming chair wearing black lace bra and panties, RGB gaming setup, purple LED lights, playful gaming pose"
        },
        "mirror": {
            "sfw": "taking mirror selfie, full body shot, bedroom mirror, purple LED strip lights, wearing black outfit",
            "nsfw": "taking mirror selfie in black lingerie, full body shot, bedroom with purple neon lights, seductive pose"
        },
        "shower": {
            "sfw": "bathroom selfie, wet hair, towel wrapped around, steamy mirror, purple mood lighting",
            "nsfw": "in shower, wet hair, water droplets on skin, steamy glass, purple ambient lighting, artistic nude"
        },
        "couch": {
            "sfw": "relaxing on couch, purple throw pillows, cozy living room, purple LED lights, wearing comfortable black clothes",
            "nsfw": "lounging on couch in black lingerie, purple throw pillows, intimate home setting, soft purple lighting"
        },
        "outdoor": {
            "sfw": "urban photoshoot, city background at night, neon signs, wearing black leather jacket and jeans, cyberpunk aesthetic",
            "nsfw": "urban rooftop at night, city lights background, wearing revealing black outfit, cyberpunk night scene"
        }
    }
    
    scenario_data = scenarios.get(scenario_type.lower(), scenarios["bedroom"])
    scenario = scenario_data["nsfw"] if nsfw else scenario_data["sfw"]
    
    return generate_luna_image(scenario, nsfw=nsfw)


def generate_custom_luna(custom_prompt: str, nsfw: bool = False) -> bytes:
    """
    Generate Luna with a completely custom scenario.
    
    Args:
        custom_prompt: Custom description of what Luna is doing/wearing/where she is
        nsfw: Whether to allow NSFW content
        
    Returns:
        bytes: PNG image data
    """
    return generate_luna_image(custom_prompt, nsfw=nsfw)

