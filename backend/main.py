from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "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"

class Chat(BaseModel):
    message: str
    tank: list | None = None


@app.post("/chat")
async def chat(data: Chat):

    try:

        # create messages list
        messages = []

        # add tank info if available
        if data.tank:
            messages.append({
                "role": "system",
                "content": f"The user's aquarium data is: {data.tank}. Give advice based on this."
            })

        # add user message
        messages.append({
            "role": "user",
            "content": data.message
        })

        # send request to OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": messages
            }
        )

        result = response.json()

        return {
            "reply": result["choices"][0]["message"]["content"]
        }

    except Exception as e:
        return {"error": str(e)}

class Settings(BaseModel):
    language: str
    notify: bool

@app.post("/save-settings")
def save_settings(data: Settings):
    return {"status": "saved", "data": data}