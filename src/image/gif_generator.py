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

# SIMPLIFIED Luna description for GIFs (much shorter to avoid 502 errors)
LUNA_GIF_BASE = "Luna Noir, 22yo woman, lavender purple bob hair, violet eyes, pale skin, goth aesthetic, photorealistic"

# GIF animation scenarios with frame descriptions
GIF_SCENARIOS = {
    "wink": {
        "name": "Sultry Wink",
        "frames": 5,
        "duration": 400,  # ms per frame
        "descriptions": [
            "sultry selfie looking at camera with both eyes open, seductive smile",
            "sultry selfie looking at camera with right eye slightly closing, seductive smile",
            "sultry selfie looking at camera with right eye closed winking, seductive smile",
            "sultry selfie looking at camera with right eye slightly opening, seductive smile",
            "sultry selfie looking at camera with both eyes open, seductive smile"
        ]
    },
    "kiss": {
        "name": "Blowing Kiss",
        "frames": 5,
        "duration": 400,
        "descriptions": [
            "sultry selfie looking at camera with seductive smile",
            "sultry selfie looking at camera with lips slightly puckered",
            "sultry selfie looking at camera blowing a kiss with puckered lips",
            "sultry selfie looking at camera with hand near lips blowing kiss",
            "sultry selfie looking at camera with seductive smile"
        ]
    },
    "pose": {
        "name": "Pose Sequence",
        "frames": 6,
        "duration": 500,
        "descriptions": [
            "standing facing camera front view, hands on hips, confident pose",
            "standing slightly turned to left, looking over shoulder at camera, confident pose",
            "standing side view profile, looking at camera, confident pose",
            "standing slightly turned to right, looking over shoulder at camera, confident pose",
            "standing facing camera front view, hands on hips, confident pose",
            "standing facing camera front view, hand in hair, seductive pose"
        ]
    },
    "tease": {
        "name": "Teasing",
        "frames": 5,
        "duration": 500,
        "descriptions": [
            "standing facing camera wearing black lace lingerie, hands at sides, seductive smile",
            "standing facing camera wearing black lace lingerie, hands touching bra strap, teasing smile",
            "standing facing camera wearing black lace lingerie, pulling bra strap down shoulder, playful smile",
            "standing facing camera topless covering breasts with hands, shy smile",
            "standing facing camera topless hands at sides revealing breasts, confident seductive smile"
        ]
    },
    "undress": {
        "name": "Undressing Sequence",
        "frames": 6,
        "duration": 600,
        "descriptions": [
            "standing facing camera wearing black lace lingerie set, hands at sides, seductive smile",
            "standing facing camera wearing black lace lingerie, hands reaching behind back to bra clasp, teasing smile",
            "standing facing camera wearing black lace bra unclasped, holding bra in place with hands, playful smile",
            "standing facing camera topless covering breasts with hands, shy smile",
            "standing facing camera topless hands lowering to sides partially revealing breasts, confident smile",
            "standing facing camera completely topless hands at sides breasts fully visible, seductive confident smile"
        ]
    },
    "dance": {
        "name": "Dancing",
        "frames": 8,
        "duration": 400,
        "descriptions": [
            "standing facing camera hands on hips, confident pose",
            "standing facing camera right hand raised above head left hand on hip, dancing pose",
            "standing facing camera both hands raised above head, dancing pose",
            "standing facing camera left hand raised above head right hand on hip, dancing pose",
            "standing facing camera hands on hips swaying, dancing pose",
            "standing facing camera right hand in hair left hand on hip, dancing pose",
            "standing facing camera both hands in hair, dancing pose",
            "standing facing camera hands on hips, confident pose"
        ]
    },
    "rotate": {
        "name": "360° Rotation",
        "frames": 8,
        "duration": 500,
        "descriptions": [
            "full length portrait showing complete body from head to feet, standing facing camera front view, hands at sides",
            "full length portrait showing complete body from head to feet, standing turned 45 degrees to left, looking at camera",
            "full length portrait showing complete body from head to feet, standing left side view profile, looking at camera",
            "full length portrait showing complete body from head to feet, standing turned 135 degrees showing back and left side, looking over shoulder",
            "full length portrait showing complete body from head to feet, standing back view showing back, looking over shoulder",
            "full length portrait showing complete body from head to feet, standing turned 225 degrees showing back and right side, looking over shoulder",
            "full length portrait showing complete body from head to feet, standing right side view profile, looking at camera",
            "full length portrait showing complete body from head to feet, standing turned 315 degrees to right, looking at camera"
        ]
    },
    "nude_tease": {
        "name": "Nude Teasing",
        "frames": 5,
        "duration": 600,
        "descriptions": [
            "standing nude facing camera covering breasts with hands and covering crotch with other hand, shy smile",
            "standing nude facing camera covering breasts with one hand other hand at side, teasing smile",
            "standing nude facing camera hands at sides breasts visible covering crotch with hand, confident smile",
            "standing nude facing camera one hand in hair other hand at side breasts and body visible, seductive smile",
            "standing nude facing camera both hands in hair fully nude body visible, confident seductive smile"
        ]
    },
    "nude_pose": {
        "name": "Nude Pose Sequence",
        "frames": 6,
        "duration": 500,
        "descriptions": [
            "standing nude facing camera front view hands on hips, confident pose",
            "standing nude turned to left looking over shoulder at camera, confident pose",
            "standing nude side view profile looking at camera, confident pose",
            "standing nude turned to right looking over shoulder at camera showing back, confident pose",
            "standing nude back view looking over shoulder at camera, confident pose",
            "standing nude facing camera front view hand in hair, seductive pose"
        ]
    }
}


def generate_gif_frame(description: str, nsfw: bool = False) -> bytes:
    """
    Generate a single GIF frame with simplified prompt to avoid 502 errors.

    Args:
        description: Short description of the frame
        nsfw: Whether to generate NSFW content

    Returns:
        bytes: PNG image data
    """
    # Build simplified prompt for GIFs
    if nsfw:
        prompt = f"{LUNA_GIF_BASE}, {description}, NSFW, 8K"
    else:
        prompt = f"{LUNA_GIF_BASE}, {description}, 8K"

    # URL encode
    encoded_prompt = quote(prompt)

    # Use consistent seed for same character
    url = f"{POLLINATIONS_API}/{encoded_prompt}?width=768&height=768&model=flux&nologo=true&seed=42"

    logger.debug(f"GIF frame URL length: {len(url)} chars")

    # Make request
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    return response.content


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

