"""
GIF Generator for Luna Noir
Creates animated GIFs from multiple Luna images
"""

import io
import logging
import requests
from urllib.parse import quote
from PIL import Image
from typing import List, Tuple

logger = logging.getLogger(__name__)

# Pollinations.ai API endpoint
POLLINATIONS_API = "https://image.pollinations.ai/prompt"

# Luna's core character description - CONSISTENT with main generator
# Using same description as luna_generator.py for character consistency
LUNA_GIF_BASE = """adult woman Luna Noir exactly 22 years old, shoulder-length lavender purple bob haircut with straight blunt bangs, almond-shaped bright violet purple eyes with thick black winged eyeliner and long black lashes, very pale porcelain white skin, heart-shaped face with high cheekbones and delicate jawline, full pouty lips with dark plum matte lipstick, small straight nose, thin black leather choker necklace, single small minimalist black outline snake tattoo on outer right forearm 8cm below elbow facing forward no other tattoos anywhere, hourglass figure with narrow waist, perky C-cup breasts, flat toned stomach, wide feminine hips, thick toned thighs, round firm bubble butt, long shapely legs, 168cm tall, athletic curvy body, goth aesthetic, seductive confident expression, sultry gaze, photorealistic"""

# Negative prompt for consistency
NEGATIVE_PROMPT = "child, teen, teenager, young girl, underage, baby face, multiple people, different hair color, blonde hair, brunette hair, long hair, curly hair, different eye color, brown eyes, blue eyes, tan skin, dark skin, anime, cartoon, 3d render, cropped, deformed, ugly, blurry, low quality, many tattoos, multiple tattoos, pixelated, low resolution, censored, plastic skin, doll face, smooth skin, airbrushed"

# GIF animation scenarios with frame descriptions
GIF_SCENARIOS = {
    "wink": {
        "name": "Sultry Wink",
        "frames": 5,  # Increased for smoother animation
        "duration": 400,  # ms per frame
        "descriptions": [
            "wearing black crop top and black ripped jeans, looking at camera both eyes open seductive smile",
            "wearing black crop top and black ripped jeans, looking at camera right eye starting to close slight smile",
            "wearing black crop top and black ripped jeans, looking at camera winking right eye fully closed playful smile",
            "wearing black crop top and black ripped jeans, looking at camera right eye opening slight smile",
            "wearing black crop top and black ripped jeans, looking at camera both eyes open seductive smile"
        ]
    },
    "kiss": {
        "name": "Blowing Kiss",
        "frames": 5,  # Increased for smoother animation
        "duration": 400,
        "descriptions": [
            "wearing black crop top and black ripped jeans, looking at camera hand at side smiling",
            "wearing black crop top and black ripped jeans, looking at camera raising hand to lips smiling",
            "wearing black crop top and black ripped jeans, looking at camera hand on lips puckered lips blowing kiss",
            "wearing black crop top and black ripped jeans, looking at camera lowering hand from lips smiling",
            "wearing black crop top and black ripped jeans, looking at camera hand at side smiling"
        ]
    },
    "pose": {
        "name": "Pose Sequence",
        "frames": 4,  # Increased for smoother animation
        "duration": 500,
        "descriptions": [
            "wearing black crop top and black ripped jeans, standing hands on hips confident pose",
            "wearing black crop top and black ripped jeans, standing one hand on hip other hand touching hair",
            "wearing black crop top and black ripped jeans, standing both hands in hair seductive pose",
            "wearing black crop top and black ripped jeans, standing hands on hips confident pose"
        ]
    },
    "tease": {
        "name": "Teasing",
        "frames": 5,  # Increased for smoother animation
        "duration": 500,
        "descriptions": [
            "wearing black lace lingerie bra and panties, standing finger on lips playful smile",
            "wearing black lace lingerie bra and panties, standing hand sliding down neck seductive smile",
            "wearing black lace lingerie bra and panties, standing hand on chest teasing smile",
            "wearing black lace lingerie bra and panties, standing hand on hip confident smile",
            "wearing black lace lingerie bra and panties, standing finger on lips playful smile"
        ]
    },
    "undress": {
        "name": "Undressing Sequence",
        "frames": 6,  # Increased for smoother animation
        "duration": 600,
        "descriptions": [
            "wearing black crop top and black lace bra underneath, standing hands at sides",
            "wearing black crop top and black lace bra underneath, standing hands gripping bottom of crop top",
            "wearing black crop top lifted up showing black lace bra, standing hands holding crop top",
            "wearing black lace bra only topless, standing hands reaching behind back to bra clasp",
            "topless covering breasts with hands, standing shy smile",
            "topless hands lowered to sides breasts visible, standing confident smile"
        ]
    },
    "dance": {
        "name": "Dancing",
        "frames": 6,  # Increased for smoother animation
        "duration": 400,
        "descriptions": [
            "wearing black crop top and black ripped jeans, dancing arms raised above head hips centered",
            "wearing black crop top and black ripped jeans, dancing arms out to sides hips swaying right",
            "wearing black crop top and black ripped jeans, dancing arms lowered hips centered",
            "wearing black crop top and black ripped jeans, dancing arms out to sides hips swaying left",
            "wearing black crop top and black ripped jeans, dancing arms raised above head hips centered",
            "wearing black crop top and black ripped jeans, dancing arms out to sides hips swaying right"
        ]
    },
    "rotate": {
        "name": "360° Rotation",
        "frames": 8,  # Increased for smoother rotation
        "duration": 400,
        "descriptions": [
            "wearing black crop top and black ripped jeans, full body standing facing camera front view",
            "wearing black crop top and black ripped jeans, full body standing turned 45 degrees right showing right side",
            "wearing black crop top and black ripped jeans, full body standing right side profile view",
            "wearing black crop top and black ripped jeans, full body standing turned 135 degrees showing back right",
            "wearing black crop top and black ripped jeans, full body standing back view facing away",
            "wearing black crop top and black ripped jeans, full body standing turned 225 degrees showing back left",
            "wearing black crop top and black ripped jeans, full body standing left side profile view",
            "wearing black crop top and black ripped jeans, full body standing turned 315 degrees showing left front"
        ]
    },
    "nude_tease": {
        "name": "Nude Teasing",
        "frames": 5,  # Increased for smoother animation
        "duration": 500,
        "descriptions": [
            "completely nude, standing covering breasts with hands and covering crotch with hand shy smile",
            "completely nude, standing covering breasts with one hand other hand lowering from crotch teasing smile",
            "completely nude, standing hands on hips breasts and body fully visible confident smile",
            "completely nude, standing one hand in hair other hand on hip seductive smile",
            "completely nude, standing covering breasts with hands and covering crotch with hand shy smile"
        ]
    },
    "nude_pose": {
        "name": "Nude Pose Sequence",
        "frames": 5,  # Increased for smoother animation
        "duration": 500,
        "descriptions": [
            "completely nude, standing hands on hips confident pose front view",
            "completely nude, standing one hand on hip other hand touching hair seductive pose",
            "completely nude, standing both hands in hair sensual pose",
            "completely nude, standing one hand on hip other hand at side confident pose",
            "completely nude, standing hands on hips confident pose front view"
        ]
    }
}


def generate_gif_frame(description: str, nsfw: bool = False, retries: int = 3) -> bytes:
    """
    Generate a single GIF frame with Luna's consistent character description.

    Args:
        description: Short description of the frame action/pose
        nsfw: Whether to generate NSFW content
        retries: Number of retry attempts on failure

    Returns:
        bytes: PNG image data
    """
    import time

    # Build prompt with full Luna description for consistency
    if nsfw:
        prompt = f"{LUNA_GIF_BASE}, {description}, professional photography, NSFW explicit, photorealistic, 8K, sharp focus"
    else:
        prompt = f"{LUNA_GIF_BASE}, {description}, professional photography, photorealistic, 8K, sharp focus"

    # URL encode the prompt
    encoded_prompt = quote(prompt)

    # URL encode the negative prompt
    encoded_negative = quote(NEGATIVE_PROMPT)

    # Use consistent seed for same character, smaller size for faster generation
    url = f"{POLLINATIONS_API}/{encoded_prompt}?width=512&height=512&model=flux&nologo=true&enhance=true&seed=42&negative={encoded_negative}"

    logger.debug(f"GIF frame URL: {url}")
    logger.debug(f"GIF frame URL length: {len(url)} chars")

    # Retry logic for errors (502, timeouts, etc.)
    last_error = None
    for attempt in range(retries):
        try:
            logger.debug(f"Attempt {attempt + 1}/{retries}")
            # Longer timeout (60s) and retry on any error
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            logger.debug(f"Frame generated successfully: {len(response.content):,} bytes")
            return response.content

        except requests.exceptions.Timeout as e:
            last_error = e
            logger.warning(f"Timeout on attempt {attempt + 1}/{retries}, retrying in 3s...")
            time.sleep(3)

        except requests.exceptions.HTTPError as e:
            last_error = e
            if e.response.status_code == 502:
                logger.warning(f"502 error on attempt {attempt + 1}/{retries}, retrying in 3s...")
                time.sleep(3)
            else:
                raise  # Re-raise non-502 HTTP errors immediately

        except Exception as e:
            last_error = e
            logger.warning(f"Error on attempt {attempt + 1}/{retries}: {type(e).__name__}: {e}")
            if attempt < retries - 1:  # Don't sleep on last attempt
                time.sleep(3)

    # All retries failed
    logger.error(f"All {retries} attempts failed for frame generation")
    raise last_error


def generate_gif_frames(scenario_type: str, nsfw: bool = False) -> List[bytes]:
    """
    Generate individual frames for a GIF animation

    Args:
        scenario_type: Type of GIF scenario (wink, kiss, pose, etc.)
        nsfw: Whether to generate NSFW content

    Returns:
        List of image bytes for each frame
    """
    if scenario_type not in GIF_SCENARIOS:
        raise ValueError(f"Unknown GIF scenario: {scenario_type}. Available: {list(GIF_SCENARIOS.keys())}")

    scenario = GIF_SCENARIOS[scenario_type]
    frames = []

    logger.info(f"Generating {scenario['frames']} frames for '{scenario['name']}' GIF (NSFW: {nsfw})")

    for i, description in enumerate(scenario['descriptions'], 1):
        logger.info(f"Generating frame {i}/{scenario['frames']}: {description[:50]}...")

        try:
            # Generate image for this frame using simplified GIF generator
            image_bytes = generate_gif_frame(description=description, nsfw=nsfw)

            frames.append(image_bytes)
            logger.info(f"Frame {i}/{scenario['frames']} generated: {len(image_bytes):,} bytes")

        except Exception as e:
            logger.error(f"Failed to generate frame {i}: {e}")
            raise

    return frames


def create_animated_gif(frames: List[bytes], duration: int = 500, loop: int = 0) -> bytes:
    """
    Create an animated GIF from a list of image frames
    
    Args:
        frames: List of image bytes for each frame
        duration: Duration of each frame in milliseconds
        loop: Number of times to loop (0 = infinite)
        
    Returns:
        Animated GIF as bytes
    """
    if not frames:
        raise ValueError("No frames provided for GIF creation")
    
    logger.info(f"Creating animated GIF from {len(frames)} frames (duration: {duration}ms, loop: {loop})")
    
    # Convert bytes to PIL Images
    pil_images = []
    for i, frame_bytes in enumerate(frames):
        try:
            img = Image.open(io.BytesIO(frame_bytes))
            # Convert to RGB if necessary (GIF doesn't support RGBA well)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            pil_images.append(img)
        except Exception as e:
            logger.error(f"Failed to process frame {i}: {e}")
            raise
    
    # Create animated GIF
    output = io.BytesIO()
    
    # Save first image with append_images for the rest
    pil_images[0].save(
        output,
        format='GIF',
        save_all=True,
        append_images=pil_images[1:],
        duration=duration,
        loop=loop,
        optimize=False  # Don't optimize to maintain quality
    )
    
    gif_bytes = output.getvalue()
    logger.info(f"Animated GIF created: {len(gif_bytes):,} bytes ({len(gif_bytes) / 1024 / 1024:.2f} MB)")
    
    return gif_bytes


def generate_luna_gif(scenario_type: str, nsfw: bool = False) -> Tuple[bytes, str]:
    """
    Generate a complete animated GIF of Luna
    
    Args:
        scenario_type: Type of GIF scenario (wink, kiss, pose, etc.)
        nsfw: Whether to generate NSFW content
        
    Returns:
        Tuple of (gif_bytes, scenario_name)
    """
    if scenario_type not in GIF_SCENARIOS:
        raise ValueError(f"Unknown GIF scenario: {scenario_type}. Available: {list(GIF_SCENARIOS.keys())}")
    
    scenario = GIF_SCENARIOS[scenario_type]
    
    logger.info(f"Starting GIF generation: '{scenario['name']}' (NSFW: {nsfw})")
    
    # Generate all frames
    frames = generate_gif_frames(scenario_type, nsfw)
    
    # Create animated GIF
    gif_bytes = create_animated_gif(frames, duration=scenario['duration'])
    
    logger.info(f"GIF generation complete: '{scenario['name']}' - {len(gif_bytes):,} bytes")
    
    return gif_bytes, scenario['name']


def get_available_gifs(nsfw: bool = False) -> dict:
    """
    Get list of available GIF scenarios
    
    Args:
        nsfw: Whether to include NSFW scenarios
        
    Returns:
        Dictionary of scenario_type -> scenario info
    """
    if nsfw:
        return GIF_SCENARIOS
    else:
        # Filter out NSFW scenarios
        return {
            k: v for k, v in GIF_SCENARIOS.items()
            if not k.startswith('nude_') and k not in ['undress', 'tease']
        }

