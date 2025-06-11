import os
import requests
from flask import Blueprint, request, jsonify

qa_bp = Blueprint('qa', __name__)

@qa_bp.route('/ask_ai', methods=['POST'])
def ask_ai():
    user_question = request.json.get('question')
    api_key = os.getenv('OPENROUTER_API_KEY')
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "messages": [{"role": "user", "content": user_question}]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=25)
        response.raise_for_status()
        answer = response.json()['choices'][0]['message']['content']
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
