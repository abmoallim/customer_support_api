from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = FastAPI()

class SupportRequest(BaseModel):
    prompt: str

# Configure the Google Gemini API
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def read_company_info():
    """Read company information from data.txt file."""
    with open("data.txt", "r") as file:
        return file.read()

def send_request_to_gemini(prompt: str):
    """Generate a response using the Gemini model."""
    company_info = read_company_info()
    
    system_message = f"""You are the best customer support AI. Use the following company information to assist customers:

{company_info}

If you cannot provide an appropriate answer, inform the customer that you cannot provide that feedback at the moment and offer to transfer them to a human agent.

You can understand the Somali language. If the customer asks a question in Somali, you should respond in Somali. Although the company data is in English, you can translate your responses into Somali where necessary.
"""


    user_message = prompt

    response = model.generate_content(f"{system_message}\n\nCustomer: {user_message}\n\nAI:")
    
    return response.text

@app.post("/api/v1/customer-support")
async def customer_support(request: SupportRequest):
    """Endpoint to handle customer support requests."""
    response = send_request_to_gemini(request.prompt)
    return {"response": response}
