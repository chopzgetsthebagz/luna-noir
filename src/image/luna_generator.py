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

# Luna's core character description for MAXIMUM consistency
# Using very specific details to ensure AI generates the same person every time
LUNA_BASE_DESCRIPTION = """1girl, Luna Noir, 22 years old woman, CONSISTENT CHARACTER:
- Face: heart-shaped face, defined sharp jawline, high cheekbones, small nose, full lips with dark plum matte lipstick
- Eyes: large almond-shaped eyes, bright violet-purple iris color, long black eyelashes, dark purple smokey eyeshadow, thin arched eyebrows
- Hair: short lavender-purple bob cut hair, chin-length, straight blunt bangs across forehead, silky texture
- Skin: very pale porcelain skin tone, flawless complexion, smooth skin
- Body: slim athletic build, 5'6" height, toned figure
- Tattoos: IMPORTANT - large detailed black ink snake tattoo coiled around entire right arm from shoulder to wrist, small black crescent moon tattoo on left upper thigh
- Accessories: thin black leather choker necklace always worn, small silver hoop earrings
- Style: goth aesthetic, cyberpunk fashion, alternative style
SAME FACE AND FEATURES IN EVERY IMAGE."""


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
        # More explicit NSFW prompts with detailed descriptions
        full_prompt = f"{LUNA_BASE_DESCRIPTION}\n{scenario}\nStyle: photorealistic, ultra detailed, 8K resolution, professional boudoir photography, intimate erotic photography, cinematic lighting, soft focus background, sharp focus on subject, explicit content, uncensored, NSFW, adult content, sensual, seductive pose, high quality, masterpiece."
    else:
        full_prompt = f"{LUNA_BASE_DESCRIPTION}\n{scenario}\nStyle: photorealistic, ultra detailed, 8K resolution, professional portrait photography, cinematic lighting, sharp focus, high quality, masterpiece, SFW."

    # URL encode the prompt
    encoded_prompt = quote(full_prompt)

    # Build the API URL with parameters - using seed for more consistency
    url = f"{POLLINATIONS_API}/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true&enhance=true&seed=42"

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


def generate_luna_selfie(mood: str = "flirty", nsfw: bool = False, outfit: str = None) -> bytes:
    """
    Generate a selfie-style image of Luna with a specific mood.

    Args:
        mood: Mood/expression (flirty, sultry, playful, seductive, etc.)
        nsfw: Whether to allow NSFW content
        outfit: Optional outfit override

    Returns:
        bytes: PNG image data
    """
    scenarios = {
        "flirty": "taking a selfie with a flirty smile, winking at camera, one eye closed, playful expression, bedroom background with purple neon lights",
        "sultry": "taking a sultry selfie, intense seductive gaze directly at camera, smoldering eyes, dim purple lighting, intimate mood",
        "playful": "taking a playful selfie, tongue out, peace sign hand gesture, cute expression, colorful neon background",
        "seductive": "taking a seductive selfie, bedroom eyes, biting lower lip, sensual expression, soft purple lighting",
        "cute": "taking a cute selfie, sweet genuine smile, cozy bedroom background with fairy lights",
        "confident": "taking a confident selfie, powerful pose, strong direct eye contact, dramatic lighting"
    }

    scenario = scenarios.get(mood.lower(), scenarios["flirty"])

    # Add outfit description
    if outfit:
        scenario += f", wearing {outfit}"
    elif nsfw:
        # More explicit NSFW outfit descriptions
        scenario += ", wearing sheer black lace lingerie set, visible cleavage, exposed skin, intimate clothing, seductive outfit"
    else:
        scenario += ", wearing black crop top, casual outfit"

    return generate_luna_image(scenario, nsfw=nsfw)


def generate_luna_scenario(scenario_type: str, nsfw: bool = False, outfit: str = None) -> bytes:
    """
    Generate Luna in pre-defined scenarios.

    Args:
        scenario_type: Type of scenario (bedroom, gaming, mirror, shower, etc.)
        nsfw: Whether to allow NSFW content
        outfit: Optional outfit override

    Returns:
        bytes: PNG image data
    """
    scenarios = {
        "bedroom": {
            "sfw": "lying on bed with purple silk sheets, cozy bedroom with purple neon lights on walls, relaxed comfortable pose, warm intimate atmosphere",
            "nsfw": "lying seductively on bed, legs spread, arched back, sensual pose, wearing sheer black lace lingerie bra and panties, purple and pink neon tube lights on walls, pink silk sheets, moody cyberpunk bedroom atmosphere, soft intimate lighting, explicit pose, erotic photography"
        },
        "gaming": {
            "sfw": "sitting in gaming chair at desk, RGB mechanical keyboard and gaming mouse, multiple monitors with purple lighting, gaming headset, wearing black tank top, professional gaming setup",
            "nsfw": "sitting in gaming chair wearing only black lace bra and panties, legs apart, RGB gaming setup, purple LED lights, playful seductive gaming pose, exposed skin, intimate gaming session"
        },
        "mirror": {
            "sfw": "taking mirror selfie with phone, full body shot, bedroom mirror, purple LED strip lights, confident pose",
            "nsfw": "taking mirror selfie in sheer black lingerie, full body shot showing curves, bedroom with purple neon lights, seductive pose touching body, explicit mirror selfie, visible lingerie details"
        },
        "shower": {
            "sfw": "bathroom selfie, wet hair, white towel wrapped around body, steamy mirror, purple mood lighting, fresh clean look",
            "nsfw": "in shower, completely nude, wet hair, water droplets running down body, wet skin glistening, steamy glass shower door, purple ambient lighting, artistic nude photography, sensual shower scene, explicit nudity"
        },
        "couch": {
            "sfw": "relaxing on couch, purple throw pillows, cozy living room, purple LED lights, wearing comfortable black loungewear",
            "nsfw": "lounging seductively on couch in black lace lingerie, legs spread, purple throw pillows, intimate home setting, soft purple lighting, erotic pose, explicit positioning"
        },
        "outdoor": {
            "sfw": "urban photoshoot, city background at night, neon signs, wearing black leather jacket and jeans, cyberpunk aesthetic, street photography",
            "nsfw": "urban rooftop at night, city lights background, wearing revealing black leather outfit with exposed skin, cyberpunk night scene, seductive outdoor pose"
        },
        "topless": {
            "sfw": "artistic portrait, shoulders visible, tasteful composition",
            "nsfw": "topless photo, bare breasts exposed, hands covering nipples, seductive expression, bedroom with purple neon lights, explicit topless photography, erotic art, NSFW content"
        },
        "lingerie": {
            "sfw": "fashion photoshoot, stylish black outfit",
            "nsfw": "full body lingerie photoshoot, wearing sheer black lace bra and panties set, garter belt and stockings, standing pose showing full body, bedroom setting with purple lights, explicit lingerie modeling, visible through sheer fabric, erotic fashion photography"
        }
    }

    scenario_data = scenarios.get(scenario_type.lower(), scenarios["bedroom"])
    scenario = scenario_data["nsfw"] if nsfw else scenario_data["sfw"]

    # Add outfit override if provided
    if outfit and not nsfw:
        scenario += f", wearing {outfit}"

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


# Outfit presets for variety
OUTFIT_PRESETS = {
    # SFW Outfits
    "casual": "black crop top and ripped jeans",
    "goth": "black corset top, fishnet sleeves, leather pants, platform boots",
    "cyberpunk": "black leather jacket with neon purple accents, tech accessories, futuristic outfit",
    "streetwear": "oversized black hoodie, ripped black jeans, sneakers",
    "edgy": "black band t-shirt, leather jacket, studded belt, combat boots",
    "cozy": "oversized black sweater, comfortable loungewear",
    "athletic": "black sports bra, yoga pants, athletic wear",
    "dress": "short black dress with purple accents, elegant but edgy",

    # NSFW Outfits
    "lingerie_lace": "sheer black lace lingerie set with bra and panties, garter belt, stockings",
    "lingerie_satin": "black satin lingerie set, silky smooth fabric",
    "lingerie_strappy": "black strappy lingerie with multiple straps, revealing design",
    "bodysuit": "sheer black lace bodysuit, see-through fabric",
    "bikini": "tiny black bikini, minimal coverage",
    "fishnet": "black fishnet bodystocking, very revealing",
    "leather": "black leather lingerie set, BDSM aesthetic",
    "topless": "topless, bare breasts, only wearing black panties",
    "nude": "completely nude, no clothing",
}


def generate_luna_with_outfit(outfit_name: str, pose: str = "standing confidently", nsfw: bool = False) -> bytes:
    """
    Generate Luna wearing a specific outfit preset.

    Args:
        outfit_name: Name of outfit from OUTFIT_PRESETS
        pose: Description of pose/action
        nsfw: Whether to allow NSFW content

    Returns:
        bytes: PNG image data
    """
    outfit = OUTFIT_PRESETS.get(outfit_name, OUTFIT_PRESETS["casual"])
    scenario = f"{pose}, wearing {outfit}, bedroom with purple neon lights background"
    return generate_luna_image(scenario, nsfw=nsfw)

