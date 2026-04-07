import os
import json
import requests

from dotenv import load_dotenv
load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def model_request(prompt: str, temperature: float, max_tokens: int):
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    resp = requests.post(OPENROUTER_URL, headers=headers, data=json.dumps(payload), timeout=60)
    resp.raise_for_status()
    return resp

def get_model_text_response(prompt: str, temperature: float = 0.3, max_tokens: int = 20000):
    response = model_request(prompt, temperature, max_tokens)
    j = response.json()
    text = j['choices'][0]['message']['content'].strip()
    return text