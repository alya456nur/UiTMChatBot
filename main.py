
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai


# --------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

frontend_dir = BASE_DIR / "frontend"


# --------------------------------------------------
# GEMINI CONFIGURATION
# --------------------------------------------------

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Please check your .env file."
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash-lite"

MAX_RETRIES = 3


# --------------------------------------------------
# CHAT MEMORY
# --------------------------------------------------

conversation_history = []


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(title="UiTM Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


# --------------------------------------------------
# GEMINI RESPONSE WITH RETRY
# --------------------------------------------------

def generate_gemini_response(prompt):

    for attempt in range(MAX_RETRIES):

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return response.text

        except Exception as e:

            error_message = str(e)

            is_temporary_error = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
            )

            if is_temporary_error and attempt < MAX_RETRIES - 1:

                wait_time = 2 ** attempt

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds "
                    f"({attempt + 1}/{MAX_RETRIES - 1})..."
                )

                time.sleep(wait_time)

            else:
                raise


# --------------------------------------------------
# CHATBOT RESPONSE
# --------------------------------------------------

def get_bot_response(user_message):

    global conversation_history

    system_prompt = """
    You are UiTM Chatbot (Universiti Teknologi MARA, Malaysia).

    Answer clearly and helpfully about:
    - UiTM courses
    - Admission
    - Campus life
    - Fees
    - General student questions

    Rules:
    - Keep answers simple and short.
    - Avoid more than 5 paragraphs.
    """

    # Add the new user message
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # Keep the latest 10 conversation messages
    conversation_history = conversation_history[-10:]

    # Build prompt
    full_prompt = system_prompt + "\n\n"

    for msg in conversation_history:

        if msg["role"] == "user":
            full_prompt += f"User: {msg['content']}\n"

        else:
            full_prompt += f"Assistant: {msg['content']}\n"

    full_prompt += "\nAssistant:"

    # Generate Gemini response with retry
    bot_reply = generate_gemini_response(full_prompt)

    # Save assistant response
    conversation_history.append({
        "role": "assistant",
        "content": bot_reply
    })

    conversation_history = conversation_history[-10:]

    return bot_reply


# --------------------------------------------------
# FRONTEND
# --------------------------------------------------

if not frontend_dir.is_dir():
    raise RuntimeError(f"Frontend folder not found: {frontend_dir}")

app.mount(
    "/frontend",
    StaticFiles(directory=str(frontend_dir)),
    name="frontend"
)


@app.get("/")
def root():
    return FileResponse(frontend_dir / "index.html")


# --------------------------------------------------
# CHAT API
# --------------------------------------------------

@app.post("/chat")
async def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:

        reply = get_bot_response(request.message)

        return {
            "reply": reply
        }

    except Exception as e:

        print("CHATBOT ERROR:", repr(e))

        error_message = str(e)

        if "503" in error_message or "UNAVAILABLE" in error_message:

            raise HTTPException(
                status_code=503,
                detail=(
                    "UiTM Chatbot is temporarily busy. "
                    "Please wait a moment and try again."
                )
            )

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating your response."
        )


# --------------------------------------------------
# TEST ENDPOINT
# --------------------------------------------------

@app.get("/api/test")
def test():

    return {
        "message": "UiTM Chatbot backend is working!"
    }
