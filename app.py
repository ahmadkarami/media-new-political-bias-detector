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

from controllers.websiteController import WebsiteController

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
JWT_SECRET = os.getenv("JWT_SECRET")

# --- Pydantic Models ---
class Message(BaseModel):
    qu: str
    an: str
    def model_dump(self) -> Dict[str, str]:
        return {"qu": self.qu, "an": self.an}

class QuestionRequest(BaseModel):
    question: str
    chat_summary: str = ""
    recent_messages: List[Message] = []
    
class ImageQuestionRequest(BaseModel):
    image_id: str
    user_id: str
    question: str
    chat_summary: str = ""
    recent_messages: List[Message] = []

# --- API Endpoints ---
@app.get("/", summary="Welcome message", description="Returns a welcome message for the RAG-based chatbot.")
def chat_bot_info():
    return 'Welcome to RAG-Based chatbot. please go to /docs for Swagger'


@app.post("/api/extract-web-text")
async def extract_web_text(data: UrlsRequest) -> List[Dict[str, Any]]:
    try:
        controller = WebsiteController()
        results = []

        for url in data.urls:
            title, text = controller.extract_text(url)
            results.append({
                "url": url,
                "text": text
            })

        return results

    except Exception as e:
        logging.error("Error in extract_web_text: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summarize-web-text")
async def summarize_web_text(data: UrlsRequest) -> List[Dict[str, Any]]:
    try:
        controller = WebsiteController()
        results = []
        responses = []
        openai = OpenAI(api_key="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", base_url="https://openrouter.ai/api/v1")

        for url in data.urls:
            title, text = controller.extract_text(url)
            results.append({
                "url": url,
                "text": text
            })
            
        # Extract just the text
        for entry in results:
            messages = [
                {"role": "system", "content": "You are a snarky assistant who summarizes news articles with wit and clarity. Your tone is clever but factual. Condense the article into 3–5 short sentences, capturing key facts, names, dates, and why it matters — while throwing in a bit of attitude, ignoring text that might be navigation related. Respond in markdown."},
                {"role": "user", "content": "The contents of this website is as follows; lease provide a short summary of this website in markdown. If it includes news or announcements, then summarize these too. " + entry["text"]}
            ]
            response = openai.chat.completions.create(model="deepseek/deepseek-r1:free", messages=messages)
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
