from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- ENV ----------------
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    print("❌ WARNING: API_KEY is not set in environment variables")

# ---------------- MODELS ----------------
class Chat(BaseModel):
    message: str
    tank: list | None = None


class Settings(BaseModel):
    language: str
    notify: bool


# ---------------- CHAT ROUTE ----------------
@app.post("/chat")
async def chat(data: Chat):

    try:
        messages = []

        # add tank context
        if data.tank:
            messages.append({
                "role": "system",
                "content": f"The user's aquarium data is: {data.tank}. Give advice based on it."
            })

        # user message
        messages.append({
            "role": "user",
            "content": data.message
        })

        # call OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": messages
            },
            timeout=30
        )

        # try parsing JSON safely
        try:
            result = response.json()
        except Exception:
            return {
                "error": "Invalid JSON response from OpenRouter",
                "raw": response.text
            }

        print("STATUS:", response.status_code)
        print("RESULT:", result)

        # handle HTTP errors
        if response.status_code != 200:
            return {
                "error": result,
                "status_code": response.status_code
            }

        # handle success
        if "choices" in result:
            return {
                "reply": result["choices"][0]["message"]["content"]
            }

        return {
            "error": "Unexpected response format",
            "raw": result
        }

    except Exception as e:
        return {
            "error": str(e)
        }


# ---------------- SETTINGS ROUTE ----------------
@app.post("/save-settings")
def save_settings(data: Settings):
    return {
        "status": "saved",
        "data": data
    }


# ---------------- HOME ROUTE ----------------
@app.get("/")
def home():
    return {
        "message": "Backend is live v2 🚀"
    }