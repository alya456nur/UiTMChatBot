import uvicorn
import webbrowser
import threading
import time
from main import app  # <-- NEW: Explicitly import your FastAPI app!

def open_browser():
    # Wait 1.5 seconds for the server to boot up, then open the browser
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000/frontend/index.html")

if __name__ == "__main__":
    # Start the browser-opening thread
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run the FastAPI server
    # <-- CHANGED: Pass the 'app' object directly instead of the string "main:app"
    uvicorn.run(app, host="127.0.0.1", port=8000)