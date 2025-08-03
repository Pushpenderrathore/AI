from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import traceback

app = Flask(__name__)
CORS(app) 

#OLLAMA_URL = os.environ.get("OLLAMA_URL", "")
OLLAMA_URL = "http://localhost:11434/api/generate"


@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get("prompt", "")
    print("Received prompt:", prompt)
    print("Using OLLAMA_URL:", OLLAMA_URL)

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": "tinyllama",
            "prompt": prompt,
            "stream": False
        } , timeout=60)
        
        response.raise_for_status()
        
        output = response.json()
        
        return jsonify({"response": output.get("response", "")})
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "✅ Flask Ollama API is working. POST to /ask"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Railway-assigned port
    app.run(host='0.0.0.0', port=port)        # Bind to all interfaces
