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

import os

API_KEY = os.getenv("API_KEY")


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

        if "choices" in result:
            return {
                "reply": result["choices"][0]["message"]["content"]
            }
        else:
            return {
                "error": result
            }

    except Exception as e:
        return {"error": str(e)}

class Settings(BaseModel):
    language: str
    notify: bool

@app.post("/save-settings")
def save_settings(data: Settings):
    return {"status": "saved", "data": data}

@app.get("/")
def home():
    return {"message": "Backend is live v2 🚀"}
