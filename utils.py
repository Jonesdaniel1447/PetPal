import os
import requests
from functools import wraps
from flask import session, redirect, url_for, flash
from app import app

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_openrouter_tips(pet):
    """Get AI-generated care tips from OpenRouter API"""
    api_key = os.environ.get('OPENROUTER_API_KEY')
    
    if not api_key:
        return {
            'error': 'OpenRouter API key not configured. Please set OPENROUTER_API_KEY environment variable.'
        }
    
    # Prepare the prompt for care tips
    prompt = f"""Please provide comprehensive care tips for a {pet.breed} {pet.species} named {pet.name}, aged {pet.age} years old. 
    
    Include specific advice for:
    1. Daily care routine
    2. Exercise requirements
    3. Grooming needs
    4. Dietary recommendations
    5. Health considerations specific to {pet.breed}
    6. Training and behavioral tips
    
    Format the response in a clear, organized manner suitable for pet owners."""
    
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3.1-8b-instruct:free",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            tips_content = data['choices'][0]['message']['content']
            
            # Parse the tips into sections
            sections = {}
            current_section = None
            current_content = []
            
            for line in tips_content.split('\n'):
                line = line.strip()
                if not line:
                    continue
                    
                # Check if line is a section header (starts with number or bullet)
                if any(line.startswith(str(i)) for i in range(1, 10)) or line.startswith('**'):
                    if current_section and current_content:
                        sections[current_section] = '\n'.join(current_content)
                    
                    # Extract section name
                    if line.startswith('**') and line.endswith('**'):
                        current_section = line.strip('*')
                    else:
                        # Extract section name from numbered list
                        parts = line.split('.', 1)
                        if len(parts) > 1:
                            current_section = parts[1].strip().rstrip(':')
                        else:
                            current_section = line
                    current_content = []
                else:
                    current_content.append(line)
            
            # Add the last section
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content)
            
            # If no sections were parsed, return the full content
            if not sections:
                sections['General Care Tips'] = tips_content
            
            return {
                'success': True,
                'breed': pet.breed,
                'sections': sections
            }
        else:
            app.logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
            return {
                'error': f'API request failed with status {response.status_code}. Please try again later.'
            }
            
    except requests.exceptions.Timeout:
        app.logger.error("OpenRouter API timeout")
        return {
            'error': 'Request timed out. Please try again later.'
        }
    except requests.exceptions.RequestException as e:
        app.logger.error(f"OpenRouter API request error: {e}")
        return {
            'error': 'Failed to connect to AI service. Please check your internet connection and try again.'
        }
    except KeyError as e:
        app.logger.error(f"OpenRouter API response parsing error: {e}")
        return {
            'error': 'Received unexpected response from AI service. Please try again later.'
        }
    except Exception as e:
        app.logger.error(f"Unexpected error in get_openrouter_tips: {e}")
        return {
            'error': 'An unexpected error occurred while generating care tips. Please try again later.'
        }
