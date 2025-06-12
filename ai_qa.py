import os
import requests
from flask import Blueprint, request, jsonify

qa_bp = Blueprint('qa', __name__)

@qa_bp.route('/ask_ai', methods=['POST'])
def ask_ai():
    user_question = request.json.get('question')
    api_key = os.getenv('GOOGLE_AI_STUDIO_API_KEY')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": user_question}
                ]
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=25)
        response.raise_for_status()
        result = response.json()
        # Gemini returns the answer in result['candidates'][0]['content']['parts'][0]['text']
        answer = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'Sorry, no answer received.')
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
