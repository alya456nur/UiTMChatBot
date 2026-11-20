# UiTM Chatbot – AI-Powered Student Assistant

An AI-powered chatbot designed to assist students and prospective students with general information about Universiti Teknologi MARA (UiTM).

The chatbot uses Google's Gemini API to generate responses to questions about UiTM courses, admissions, campus life, fees, and general student-related topics.

## About the Project

UiTM Chatbot is a web-based conversational assistant developed to provide users with a simple way to ask questions about UiTM.

The application combines a Python-based backend with a web-based chat interface. Users can enter questions through the chat interface and receive AI-generated responses.

## Features

- Interactive chatbot interface
- AI-generated responses using Google Gemini
- Answers questions about UiTM courses
- Provides general admission information
- Assists with campus life enquiries
- Answers questions about fees
- Supports general student-related questions
- Maintains conversation context
- Automatically opens the chatbot in a web browser when launched

## Technologies Used

**Frontend**
- HTML5
- CSS3
- JavaScript
- Font Awesome
- Marked.js

**Backend**
- Python
- FastAPI
- Uvicorn
- Pydantic

**AI Integration**
- Google Gemini API
- Google Generative AI Python SDK

**Other Tools**
- python-dotenv
- PyInstaller

## Project Structure

```text
UiTMChatBot/
│
├── frontend/
│   ├── index.html          # Chatbot interface
│   ├── style.css           # Chatbot styling
│   ├── script.js           # Chat functionality
│   ├── logo.png            # Chatbot logo
│   └── logo2.jpg           # Additional logo image
│
├── main.py                 # FastAPI backend and AI integration
├── run.py                  # Application launcher
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore
├── UiTMBot.spec            # PyInstaller configuration
└── README.md
```

## Getting Started

### Prerequisites

Make sure you have installed:

- Python 3.10 or later
- pip
- Google Gemini API key

### 1. Clone the Repository

```bash
git clone https://github.com/alya456nur/UiTMChatBot.git
```

Navigate into the project directory:

```bash
cd uitmchatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows:**

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a template.

Add your Google Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Replace the placeholder with your own API key.

**Important:** Never upload your actual `.env` file or expose your API key on GitHub.

### 5. Run the Application

Start the chatbot:

```bash
python run.py
```

The application starts the FastAPI server and automatically opens the chatbot in your default web browser.

Alternatively, access it at:

```text
http://127.0.0.1:8000
```

## How It Works

1. The user enters a question through the web-based chat interface.
2. JavaScript sends the message to the FastAPI backend.
3. The backend combines the question with the chatbot's system instructions and recent conversation history.
4. The Google Gemini API generates a response.
5. The response is returned to the frontend and displayed in the chat interface.

## AI Integration

The chatbot uses Google's Gemini API to generate conversational responses.

Its system instructions focus on UiTM-related topics, including:

- Courses
- Admissions
- Campus life
- Fees
- General student enquiries

The application also maintains a limited conversation history to provide conversational context.

## Developer

Developed as an academic project.
