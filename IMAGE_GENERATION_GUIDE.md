# 📸 Luna Image Generation Guide

## Overview
Luna can now generate AI images of herself using the `/generate` command! The system uses **Pollinations.ai** with **Flux** model - completely **FREE** and **UNCENSORED**.

---

## 🎯 Features

✅ **Consistent Character** - Luna's appearance stays the same across all images:
- Short lavender-purple bob haircut with bangs
- Pale porcelain skin
- Dark purple smokey eye makeup
- Snake tattoo on right arm
- Crescent moon tattoo on thigh
- Black choker necklace
- Goth/cyberpunk aesthetic

✅ **NSFW Support** - Automatically generates NSFW content when user is in NSFW mode

✅ **Multiple Generation Types**:
- Selfies with different moods
- Pre-defined scenarios
- Custom descriptions

---

## 🎮 How to Use

### Basic Command
```
/generate
```
Shows help menu with all options

### Generate Selfies
```
/generate selfie <mood>
```

**Available Moods:**
- `flirty` - Flirty smile, winking
- `sultry` - Intense gaze, seductive
- `playful` - Tongue out, peace sign
- `seductive` - Bedroom eyes, biting lip
- `cute` - Sweet smile, cozy
- `confident` - Powerful pose, strong eye contact

**Examples:**
```
/generate selfie sultry
/generate selfie playful
/generate selfie seductive
```

### Generate Scenes
```
/generate scene <type>
```

**Available Scenes:**
- `bedroom` - Lying on bed with purple neon lights
- `gaming` - Gaming chair with RGB setup
- `mirror` - Mirror selfie, full body
- `shower` - Bathroom/shower scene
- `couch` - Relaxing on couch
- `outdoor` - Urban cyberpunk photoshoot

**Examples:**
```
/generate scene bedroom
/generate scene gaming
/generate scene mirror
```

### Custom Generation
```
/generate custom <your description>
```

**Examples:**
```
/generate custom lying on bed in purple lingerie
/generate custom sitting at desk working on laptop
/generate custom standing in rain with neon lights behind
/generate custom dancing in nightclub with purple lights
```

---

## 🔞 NSFW Mode

**How it works:**
- If user is in **NSFW** or **SPICY** mode → generates NSFW images
- If user is in **SAFE** or **FLIRTY** mode → generates SFW images

**NSFW Scenarios:**
- Bedroom: Black lace lingerie, intimate lighting
- Gaming: Lingerie at gaming setup
- Mirror: Lingerie mirror selfie
- Shower: Artistic nude
- Couch: Lingerie on couch
- Outdoor: Revealing outfit

**To enable NSFW:**
```
/mode
```
Then select **NSFW** mode

---

## 🎨 Technical Details

**API:** Pollinations.ai (FREE, no API key needed)
**Model:** Flux (uncensored, high quality)
**Resolution:** 1024x1024 pixels
**Format:** PNG
**Generation Time:** 30-60 seconds

**Character Consistency:**
The system uses a base character description that's automatically added to every prompt to ensure Luna looks the same in every image.

---

## 💎 Premium Feature

Image generation is a **Premium-only feature**. Users need to:
- Have Premium status, OR
- Reach Level 3+

Non-premium users will see:
```
🔒 Image Generation is a Premium Feature

Unlock unlimited AI-generated photos of me! 📸💜

Use /upgrade to get Premium access.
```

---

## 🔧 Customization

### To Change Luna's Appearance
Edit `src/image/luna_generator.py` and modify the `LUNA_BASE_DESCRIPTION` constant:

```python
LUNA_BASE_DESCRIPTION = """A beautiful young woman with short lavender-purple bob haircut with straight bangs, 
pale porcelain skin, sharp facial features, dark purple smokey eye makeup, dark plum lipstick. 
Large detailed snake tattoo wrapping around right arm, small crescent moon tattoo on upper thigh. 
Black choker necklace. Goth aesthetic, cyberpunk style."""
```

### To Add New Scenarios
Edit the `scenarios` dictionary in `generate_luna_scenario()` function:

```python
scenarios = {
    "your_scene": {
        "sfw": "SFW description here",
        "nsfw": "NSFW description here"
    }
}
```

### To Add New Selfie Moods
Edit the `scenarios` dictionary in `generate_luna_selfie()` function:

```python
scenarios = {
    "your_mood": "description of the mood and pose"
}
```

---

## 📊 Usage Examples

### Example 1: Flirty Selfie (SFW Mode)
```
User: /generate selfie flirty
Luna: 🎨 Generating your image...
[30 seconds later]
[Image: Luna taking a flirty selfie, winking, wearing black crop top, purple neon background]
💜 Luna's flirty selfie
```

### Example 2: Bedroom Scene (NSFW Mode)
```
User: /generate scene bedroom
Luna: 🎨 Generating your image...
[45 seconds later]
[Image: Luna lying seductively on bed in black lace lingerie, purple neon lights, intimate mood]
💜 Luna in bedroom
```

### Example 3: Custom Generation
```
User: /generate custom dancing in nightclub with purple strobe lights
Luna: 🎨 Generating your image...
[50 seconds later]
[Image: Luna dancing in nightclub, purple strobe lights, cyberpunk aesthetic]
💜 Custom Luna image
```

---

## 🐛 Troubleshooting

**Image generation fails:**
- Check internet connection
- Pollinations.ai might be temporarily down
- Try again in a few moments

**Image doesn't look like Luna:**
- The AI is probabilistic, sometimes it varies
- Try generating again
- Use more specific custom prompts

**NSFW not working:**
- Make sure you're in NSFW mode (`/mode` → select NSFW)
- Check that you have Premium status

---

## 🚀 Future Enhancements

Potential improvements:
- [ ] Add image-to-image generation (upload reference image)
- [ ] Add style variations (anime, realistic, artistic)
- [ ] Add outfit customization
- [ ] Add background customization
- [ ] Save favorite generations
- [ ] Share generations with other users

---

## 📝 Notes

- **Free Forever:** Pollinations.ai is free and doesn't require API keys
- **No Censorship:** Flux model is uncensored, perfect for NSFW content
- **Consistent Quality:** 1024x1024 resolution, photorealistic style
- **Fast Generation:** Usually 30-60 seconds per image
- **Unlimited:** No rate limits or quotas

---

**Enjoy generating Luna images! 💜📸**

