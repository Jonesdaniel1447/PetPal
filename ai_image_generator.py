import os
import requests
import base64
from datetime import datetime

GOOGLE_AI_STUDIO_API_KEY = os.environ.get("GOOGLE_AI_STUDIO_API_KEY")
GOOGLE_AI_STUDIO_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagegeneration:generate"  # Example endpoint, update if needed

# Available art styles for pet profile generation
ART_STYLES = {
    'realistic': {
        'name': 'Realistic Portrait',
        'description': 'Photorealistic style with natural lighting',
        'prompt_suffix': 'photorealistic, professional pet photography, natural lighting, high detail, studio quality'
    },
    'cartoon': {
        'name': 'Cartoon Style',
        'description': 'Fun animated cartoon style',
        'prompt_suffix': 'cartoon style, animated, colorful, Disney-Pixar style, cute and expressive'
    },
    'watercolor': {
        'name': 'Watercolor Painting',
        'description': 'Soft watercolor artistic style',
        'prompt_suffix': 'watercolor painting, soft brush strokes, artistic, pastel colors, painted texture'
    },
    'oil_painting': {
        'name': 'Oil Painting',
        'description': 'Classic oil painting style',
        'prompt_suffix': 'oil painting, classical art style, rich colors, textured brush strokes, museum quality'
    },
    'digital_art': {
        'name': 'Digital Art',
        'description': 'Modern digital illustration',
        'prompt_suffix': 'digital art, modern illustration, vibrant colors, clean lines, contemporary style'
    },
    'fantasy': {
        'name': 'Fantasy Style',
        'description': 'Magical fantasy artwork',
        'prompt_suffix': 'fantasy art, magical elements, ethereal lighting, mystical atmosphere, enchanted'
    },
    'minimalist': {
        'name': 'Minimalist',
        'description': 'Clean minimalist design',
        'prompt_suffix': 'minimalist style, simple lines, clean design, geometric, modern art'
    },
    'vintage': {
        'name': 'Vintage Portrait',
        'description': 'Classic vintage photography style',
        'prompt_suffix': 'vintage style, sepia tones, classic photography, nostalgic, retro aesthetic'
    }
}

def generate_pet_profile_picture(pet_name, pet_species, pet_breed, art_style='realistic', additional_details=''):
    """Generate a custom profile picture for a pet using Google AI Studio"""
    try:
        if not GOOGLE_AI_STUDIO_API_KEY:
            raise ValueError("Google AI Studio API key not configured")

        style_config = ART_STYLES.get(art_style, ART_STYLES['realistic'])
        base_prompt = f"A beautiful portrait of a {pet_breed} {pet_species} named {pet_name}"
        if additional_details:
            base_prompt += f", {additional_details}"
        full_prompt = f"{base_prompt}, {style_config['prompt_suffix']}"

        # Google AI Studio API request (update payload/endpoint as needed)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GOOGLE_AI_STUDIO_API_KEY}"
        }
        payload = {
            "prompt": full_prompt,
            "num_images": 1,
            "image_size": "512x512"
        }
        response = requests.post(GOOGLE_AI_STUDIO_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        # Adapt this extraction if Google API response differs
        image_url = None
        if 'images' in data and data['images']:
            image_url = data['images'][0]['url']
        elif 'data' in data and data['data'] and 'url' in data['data'][0]:
            image_url = data['data'][0]['url']
        image_filename = save_generated_image(image_url, pet_name, art_style) if image_url else None

        if image_filename:
            return {
                'success': True,
                'image_url': image_url,
                'image_filename': image_filename,
                'prompt_used': full_prompt,
                'style_used': style_config['name']
            }
        else:
            return {
                'success': False,
                'error': 'Failed to save generated image'
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def save_generated_image(image_url, pet_name, art_style):
    """Download and save the generated image locally"""
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = 'static/uploads/generated'
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_pet_name = "".join(c for c in pet_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{safe_pet_name}_{art_style}_{timestamp}.png"
        filepath = os.path.join(upload_dir, filename)
        
        # Download the image
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # Save the image
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        # Return relative path for web use
        return f"uploads/generated/{filename}"
        
    except Exception as e:
        print(f"Error saving generated image: {e}")
        return None

def generate_pet_variations(pet_name, pet_species, pet_breed, base_style='realistic', num_variations=3):
    """Generate multiple variations of a pet profile picture"""
    variations = []
    
    # Different variation prompts
    variation_prompts = [
        f"close-up portrait",
        f"full body portrait",
        f"artistic headshot with beautiful background"
    ]
    
    for i, variation_prompt in enumerate(variation_prompts[:num_variations]):
        result = generate_pet_profile_picture(
            pet_name=pet_name,
            pet_species=pet_species,
            pet_breed=pet_breed,
            art_style=base_style,
            additional_details=variation_prompt
        )
        
        if result['success']:
            variations.append({
                'variation_type': variation_prompt,
                'image_filename': result['image_filename'],
                'image_url': result['image_url']
            })
    
    return variations

def get_style_preview_prompts():
    """Get sample prompts for style previews"""
    return {
        style_key: {
            'name': style_data['name'],
            'description': style_data['description'],
            'sample_prompt': f"A golden retriever dog, {style_data['prompt_suffix']}"
        }
        for style_key, style_data in ART_STYLES.items()
    }
