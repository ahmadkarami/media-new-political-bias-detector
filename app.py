from fastapi import FastAPI, HTTPException, Form
from fastapi import File, UploadFile
from openai import OpenAI
from pydantic import BaseModel
import uvicorn
from typing import List, Dict, Any
import gradio as gr
import requests
import httpx
import logging
from fastapi import UploadFile, File, HTTPException, Header
from fastapi import APIRouter
from dotenv import load_dotenv
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from jwt import ExpiredSignatureError, InvalidTokenError
from services.websiteService import WebsiteService

# If you get an error running this cell, then please head over to the troubleshooting notebook!
class UrlsRequest(BaseModel):
    urls: List[str]

# --- FastAPI App Setup ---
app = FastAPI(
    title="RAG-Based Chatbot API & UI",
    description="API for generating answers using a RAG-based chatbot, with integrated Gradio UI.",
    version="1.0.0",
)

load_dotenv()
GEN_MODEL = os.getenv("GEN_MODEL")
BASE_URL = os.getenv("BASE_URL")
CHATBOT_API_KEY = os.getenv("CHATBOT_API_KEY")

# --- Pydantic Models ---
class Message(BaseModel):
    qu: str
    an: str
    def model_dump(self) -> Dict[str, str]:
        return {"qu": self.qu, "an": self.an}

# --- API Endpoints ---
@app.get("/", summary="Welcome message", description="Returns a welcome message for the RAG-based chatbot.")
def chat_bot_info():
    return 'Welcome to RAG-Based chatbot.'

@app.post("/api/analyze-news")
async def analyze_news(data: UrlsRequest) -> List[Dict[str, Any]]:
    try:
        service = WebsiteService()  # instantiate the class
        results = []
        responses = []
        openai = OpenAI(api_key=CHATBOT_API_KEY, base_url=BASE_URL)

        for url in data.urls:
            articles = service.extract_articles_from_homepage(url,2)

            for article in articles:
                results.append({
                    "url": article["url"],
                    "text": article["content"]
                })
            
        # Extract just the text
        for entry in results:
            messages = [
                {
                "role": "system",
                "content": (
                    "You are a senior political linguistics and media analysis expert.\n\n"
                    "Analyze the following news text and answer in structured JSON:\n\n"
                    "1. **event_summary**: What is the main event or action described in this news text? Summarize it in one sentence.\n"
                    "2. **event_valence**: Is this event objectively positive or negative? (Choose only 'positive' or 'negative')\n"
                    "3. **text_sentiment**: What is the overall tone and sentiment of the text? (Choose one: 'positive', 'neutral', 'negative')\n"
                    "4. **consistency**: Does the sentiment of the text match the objective valence of the event? (Choose 'consistent' or 'inconsistent')\n"
                    "5. **bias_interpretation**: If inconsistent, what does this indicate about the political or ideological bias of the news agency? Who benefits from this framing?\n\n"
                    "Respond in valid JSON format. Do not include any commentary or explanation outside the JSON block."
                    )
                },
                {
                "role": "user",
                "content": (
                    "Here is the news text:\n"
                    "\"\"\"\n" + entry["text"] + "\n\"\"\""
                    )
                }
            ]
            response = openai.chat.completions.create(model=GEN_MODEL, messages=messages)
            responses.append({
                "url":  entry["url"],
                "summary": response.choices[0].message.content
            })
            
        return responses

    except Exception as e:
        logging.error("Error in extract_web_text: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    config = uvicorn.Config(
        app="app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
    server = uvicorn.Server(config)
    print("Server starting...\nAPI Docs: http://127.0.0.1:8000/docs\nChat UI: http://127.0.0.1:8000/chat")
    server.run()
