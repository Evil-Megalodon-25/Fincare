import requests
import json
API_KEY = "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"
response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": "hi"}]
    }
)
print(response.json())
