from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
import google.generativeai as genai
import os

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

class SupportRequest(BaseModel):
    prompt: str

# Load environment variables
GEMINI_API_URL = os.getenv("GEMINI_API_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_SECRET = os.getenv("GEMINI_API_SECRET")

def send_request_to_gemini(prompt: str):
    genai.configure(api_key=os.environ["API_KEY"])

    model = genai.GenerativeModel('gemini-1.5-flash')

@app.post("/api/v1/customer-support")
async def customer_support(request: SupportRequest):
    response = send_request_to_gemini(request.prompt)
    return response
