from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get("prompt", "")

    response = requests.post(OLLAMA_URL, json={
        "model": "tinyllama",
        "prompt": prompt,
        "stream": False
    })

    output = response.json()
    return jsonify({"response": output.get("response", "")})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
