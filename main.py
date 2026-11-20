from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai
import sys
import os
from dotenv import load_dotenv

# --- NEW: PyInstaller Path Helper ---
def get_resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # If not running as .exe, use the normal current directory
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini model 
model = genai.GenerativeModel("gemini-3.5-flash")

# Chat memory 
conversation_history = []

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ChatRequest(BaseModel):
    message: str

# UiTM chatbot response function
def get_bot_response(user_message):
    global conversation_history

    # Save user message
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # Keep only last 10 user/bot exchanges to manage memory
    conversation_history = conversation_history[-10:]

    # System prompt
    system_prompt = """
    You are UiTM Chatbot (Universiti Teknologi MARA, Malaysia).

    Answer clearly and helpfully about:
    - UiTM courses
    - admission
    - campus life
    - fees
    - general student questions

    Rules:
    - Keep answers simple and short
    - Avoid more than 5 paragraphs
    """

    # Build conversation text
    full_prompt = system_prompt + "\n\n"

    for msg in conversation_history:
        if msg["role"] == "user":
            full_prompt += f"User: {msg['content']}\n"
        else:
            full_prompt += f"Assistant: {msg['content']}\n"

    full_prompt += "Assistant:"

    # Generate response
    response = model.generate_content(full_prompt)

    bot_reply = response.text

    # Save bot response
    conversation_history.append({
        "role": "assistant",
        "content": bot_reply
    })

    return bot_reply



    return os.path.join(base_path, relative_path)

frontend_dir = get_resource_path("frontend")

# 1. Mount the frontend folder using the dynamic path
app.mount("/frontend", StaticFiles(directory=frontend_dir), name="frontend")

# 2. Serve the main HTML interface using the dynamic path
@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

# Chat endpoint
@app.post("/chat")
async def chat(request: ChatRequest):
    reply = get_bot_response(request.message)
    return {"reply": reply}