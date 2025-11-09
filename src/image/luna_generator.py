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

# Luna's core character description - ULTRA SPECIFIC for maximum consistency
# IMPORTANT: Luna is clearly an adult woman (22 years old) with sexy proportions
LUNA_BASE_DESCRIPTION = """adult woman Luna Noir exactly 22 years old, mature feminine features, shoulder-length lavender purple bob haircut with perfectly straight blunt bangs across forehead, almond-shaped bright violet purple eyes with thick black winged eyeliner, very pale porcelain white skin with natural skin texture and pores, heart-shaped face with high defined cheekbones, full pouty lips with dark plum lipstick, thin black leather choker necklace around neck, single small simple black line art snake tattoo on right forearm only no other tattoos, hourglass figure with narrow waist, perky C-cup breasts with soft pink nipples and small areolas, flat toned stomach with subtle abs, wide feminine hips, thick toned thighs, round firm bubble butt, long shapely legs, 168cm tall 5foot6, athletic curvy body type, goth aesthetic, seductive confident expression, sultry gaze, photorealistic human features"""

# Negative prompt to avoid inconsistencies and ensure adult appearance
NEGATIVE_PROMPT = "child, teen, teenager, young girl, underage, baby face, multiple people, crowd, group, different hair color, blonde hair, brunette hair, long hair, curly hair, different eye color, brown eyes, blue eyes, green eyes, tan skin, dark skin, tanned, muscular, overweight, flat chest, elderly, old, anime, cartoon, 3d render, cropped head, cropped feet, cut off, partial body, deformed, ugly, blurry, low quality, many tattoos, multiple tattoos, face tattoos, neck tattoos, chest tattoos, breast tattoos, stomach tattoos, back tattoos, leg tattoos, sleeve tattoos, arm sleeve, full sleeve, colorful tattoos, large tattoos, pixelated, censored, blurred face, plastic skin, doll face, artificial, fake skin, smooth skin, airbrushed, oversaturated, deformed breasts, deformed nipples, missing nipples, extra nipples, weird nipples, large nipples, dark nipples, inverted nipples, asymmetric nipples, unnatural nipples, pointy nipples, cone shaped breasts, strange nipples, malformed nipples, distorted nipples, bad anatomy, bad breasts, ugly breasts, fake breasts, implants, bolt-on breasts"


def generate_luna_image(scenario: str, nsfw: bool = False, width: int = 1536, height: int = 1536, seed: int = None) -> bytes:
    """
    Generate an image of Luna in a specific scenario.

    Args:
        scenario: Description of the scene/pose/outfit (e.g., "lying on bed in lingerie")
        nsfw: Whether to allow NSFW content
        width: Image width (default 1536 - high resolution)
        height: Image height (default 1536 - high resolution)
        seed: Random seed for reproducibility (None = random)

    Returns:
        bytes: PNG image data

    Raises:
        requests.HTTPError: If API request fails
    """
    # Adjust dimensions for full body shots - MUCH taller aspect ratio with HIGH RESOLUTION
    if "full body" in scenario.lower() or "head to toe" in scenario.lower() or "standing" in scenario.lower():
        width = 1024   # Narrower for full body portraits (high res)
        height = 2048  # Much taller to ensure feet are visible (high res)
        # Add explicit framing instruction
        scenario = f"full length portrait showing complete body from top of head to bottom of feet, {scenario}"

    # Build the full prompt with Luna's consistent features
    # Always emphasize adult woman to ensure mature appearance
    if nsfw:
        # NSFW prompts - CONCISE but specific for nipples and tattoo
        full_prompt = f"{LUNA_BASE_DESCRIPTION}, {scenario}, professional nude photography, soft pink nipples, single snake tattoo right forearm, natural lighting, NSFW explicit, photorealistic, 8K, uncensored"
    else:
        full_prompt = f"{LUNA_BASE_DESCRIPTION}, {scenario}, single snake tattoo right forearm, photorealistic, professional photography, 8K, sharp focus"

    # URL encode the prompt
    encoded_prompt = quote(full_prompt)

    # Use consistent seed for same character appearance
    # Seed 42 ensures Luna looks the same across all images
    seed_param = f"&seed={seed}" if seed is not None else "&seed=42"

    # Build the API URL with parameters - HIGH RESOLUTION with natural features
    url = f"{POLLINATIONS_API}/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true&enhance=true{seed_param}"

    logger.info(f"Generating Luna image: {scenario[:50]}... (NSFW: {nsfw}, {width}x{height})")

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
        "flirty": "selfie, winking, playful smile, purple neon lights",
        "sultry": "selfie, intense gaze, seductive eyes, dim purple lighting",
        "playful": "selfie, tongue out, peace sign, colorful neon background",
        "seductive": "selfie, bedroom eyes, biting lip, soft purple lighting",
        "cute": "selfie, sweet smile, cozy bedroom, fairy lights",
        "confident": "selfie, powerful pose, direct eye contact, dramatic lighting"
    }

    scenario = scenarios.get(mood.lower(), scenarios["flirty"])

    # Add outfit description
    if outfit:
        scenario += f", {outfit}"
    elif nsfw:
        scenario += ", black lace lingerie"
    else:
        scenario += ", black crop top"

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
            "sfw": "lying on bed, purple silk sheets, purple neon lights, relaxed pose",
            "nsfw": "lying seductively on bed, legs spread, sheer black lingerie, purple neon lights, intimate pose"
        },
        "gaming": {
            "sfw": "sitting in gaming chair, RGB setup, purple lighting, black tank top",
            "nsfw": "sitting in gaming chair, black lace bra and panties, RGB lights, playful seductive pose"
        },
        "mirror": {
            "sfw": "mirror selfie, full body, purple LED lights, confident pose",
            "nsfw": "mirror selfie in sheer lingerie, full body showing curves, purple lights, seductive pose"
        },
        "shower": {
            "sfw": "bathroom, wet hair, white towel, steamy mirror, purple lighting",
            "nsfw": "in shower fully naked, wet skin, water running down body, steamy glass, purple lighting"
        },
        "couch": {
            "sfw": "relaxing on couch, purple pillows, purple LED lights, black loungewear",
            "nsfw": "lounging on couch in black lace lingerie, legs spread, purple pillows, intimate lighting"
        },
        "outdoor": {
            "sfw": "urban night, neon signs, black leather jacket and jeans, cyberpunk aesthetic",
            "nsfw": "urban rooftop, city lights, revealing leather outfit with skin exposed, night scene"
        },
        "topless": {
            "sfw": "artistic portrait, shoulders visible, tasteful composition",
            "nsfw": "topless with bare chest exposed, natural pose, bedroom, purple neon lights"
        },
        "fullbody": {
            "sfw": "standing pose, wearing black crop top and ripped jeans, purple neon background, camera pulled back to show entire body",
            "nsfw": "standing straight with arms at sides, completely naked, bedroom with purple neon lights, camera angle showing complete nude body"
        },
        "nude": {
            "sfw": "artistic silhouette, tasteful shadows",
            "nsfw": "standing straight with hands at sides, completely naked, bedroom, soft purple lighting, frontal view"
        },
        "nude_lying": {
            "sfw": "lying on bed, comfortable pose, bedroom",
            "nsfw": "lying naked on back, legs spread wide, pink silk sheets, purple lights, intimate view"
        },
        "nude_sitting": {
            "sfw": "sitting pose, casual setting",
            "nsfw": "sitting naked on bed edge, legs spread apart, bedroom, purple lights, intimate angle"
        },
        "nude_kneeling": {
            "sfw": "kneeling pose, artistic composition",
            "nsfw": "kneeling naked on bed, arched back, chest forward, bedroom, soft purple lighting"
        },
        "nude_bent_over": {
            "sfw": "artistic pose, implied sensuality",
            "nsfw": "bent over naked on hands and knees, rear view, looking back over shoulder, bedroom, purple lights"
        },
        "nude_side_view": {
            "sfw": "side profile portrait, artistic lighting",
            "nsfw": "side view standing naked, full body profile, one leg forward, bedroom, purple lighting"
        },
        "lingerie": {
            "sfw": "fashion photoshoot, stylish black outfit",
            "nsfw": "full body in sheer black lace lingerie set, garter belt and stockings, bedroom, purple lights"
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

