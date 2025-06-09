"""
Demo image generator for showcasing AI Profile Picture Generator functionality
This creates sample generated images to demonstrate the feature when API key is not available
"""

import os
from PIL import Image, ImageDraw, ImageFont
import random

def create_demo_profile_picture(pet_name, pet_species, pet_breed, art_style='realistic'):
    """Create a demo profile picture with pet information and art style"""
    
    # Create uploads directory if it doesn't exist
    upload_dir = 'static/uploads/generated'
    os.makedirs(upload_dir, exist_ok=True)
    
    # Image dimensions
    width, height = 512, 512
    
    # Style-specific colors and patterns
    style_configs = {
        'realistic': {'bg_color': (245, 245, 245), 'text_color': (50, 50, 50), 'accent': (74, 144, 226)},
        'cartoon': {'bg_color': (255, 230, 200), 'text_color': (80, 50, 30), 'accent': (255, 140, 100)},
        'watercolor': {'bg_color': (240, 248, 255), 'text_color': (70, 80, 120), 'accent': (120, 150, 200)},
        'oil_painting': {'bg_color': (250, 240, 230), 'text_color': (80, 60, 40), 'accent': (160, 120, 80)},
        'digital_art': {'bg_color': (230, 230, 250), 'text_color': (60, 60, 100), 'accent': (120, 120, 200)},
        'fantasy': {'bg_color': (240, 230, 255), 'text_color': (80, 50, 100), 'accent': (150, 100, 200)},
        'minimalist': {'bg_color': (248, 248, 248), 'text_color': (100, 100, 100), 'accent': (150, 150, 150)},
        'vintage': {'bg_color': (245, 235, 220), 'text_color': (80, 70, 60), 'accent': (140, 120, 100)}
    }
    
    config = style_configs.get(art_style, style_configs['realistic'])
    
    # Create image
    img = Image.new('RGB', (width, height), config['bg_color'])
    draw = ImageDraw.Draw(img)
    
    # Try to use a better font, fall back to default if not available
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw decorative elements based on art style
    if art_style == 'realistic':
        # Simple camera icon representation
        draw.rectangle([width//2-60, height//2-60, width//2+60, width//2+60], 
                      outline=config['accent'], width=3)
        draw.ellipse([width//2-30, height//2-30, width//2+30, width//2+30], 
                    outline=config['accent'], width=2)
    elif art_style == 'cartoon':
        # Playful shapes
        for i in range(5):
            x = random.randint(50, width-50)
            y = random.randint(50, height-50)
            size = random.randint(20, 40)
            draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], 
                        fill=config['accent'], outline=None)
    elif art_style == 'watercolor':
        # Soft circular patterns
        for i in range(8):
            x = random.randint(100, width-100)
            y = random.randint(100, height-100)
            size = random.randint(30, 80)
            color = (*config['accent'], 50)  # Semi-transparent
            draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], 
                        fill=color, outline=None)
    
    # Draw pet paw icon in center
    paw_size = 80
    paw_x, paw_y = width//2, height//2
    
    # Main paw pad
    draw.ellipse([paw_x-25, paw_y-10, paw_x+25, paw_y+30], 
                fill=config['accent'], outline=None)
    
    # Toe pads
    positions = [(-20, -25), (-5, -30), (10, -30), (25, -25)]
    for px, py in positions:
        draw.ellipse([paw_x+px-8, paw_y+py-8, paw_x+px+8, paw_y+py+8], 
                    fill=config['accent'], outline=None)
    
    # Add text information
    y_offset = height - 120
    
    # Pet name
    name_text = pet_name
    draw.text((width//2, y_offset), name_text, font=font_large, 
             fill=config['text_color'], anchor="mm")
    
    # Species and breed
    breed_text = f"{pet_breed} {pet_species}"
    draw.text((width//2, y_offset + 40), breed_text, font=font_medium, 
             fill=config['text_color'], anchor="mm")
    
    # Art style label
    style_text = f"{art_style.replace('_', ' ').title()} Style"
    draw.text((width//2, y_offset + 70), style_text, font=font_small, 
             fill=config['accent'], anchor="mm")
    
    # Demo watermark
    draw.text((width//2, 30), "DEMO - AI Generated", font=font_small, 
             fill=config['accent'], anchor="mm")
    
    # Save the image
    timestamp = random.randint(100000, 999999)  # Use random number for demo
    safe_pet_name = "".join(c for c in pet_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    filename = f"demo_{safe_pet_name}_{art_style}_{timestamp}.png"
    filepath = os.path.join(upload_dir, filename)
    
    img.save(filepath, 'PNG')
    
    return f"uploads/generated/{filename}"

def create_demo_variations(pet_name, pet_species, pet_breed, base_style='realistic'):
    """Create demo variations of a pet profile picture"""
    variations = []
    
    variation_styles = ['close-up portrait', 'full body portrait', 'artistic headshot']
    
    for i, variation_type in enumerate(variation_styles):
        # Create a slightly different demo image for each variation
        filename = create_demo_profile_picture(pet_name, pet_species, pet_breed, base_style)
        
        variations.append({
            'variation_type': variation_type,
            'image_filename': filename,
            'image_url': f'/static/{filename}'
        })
    
    return variations