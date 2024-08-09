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

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def read_company_info():
    with open("data.txt", "r") as file:
        return file.read()



# def send_request_to_gemini(prompt: str):
#     response = model.generate_content(prompt)
#     return response.text

def send_request_to_gemini(prompt: str):
    company_info = read_company_info()
    
    system_message = f"""You are the best customer support AI. Use the following company information to assist customers:

{company_info}

If you cannot provide an appropriate answer, inform the customer that you cannot provide that feedback at the moment and offer to transfer them to a human agent."""

    user_message = prompt

    response = model.generate_content(f"{system_message}\n\nCustomer: {user_message}\n\nAI:")
    
    return response.text



@app.post("/api/v1/customer-support")
async def customer_support(request: SupportRequest):
    response = send_request_to_gemini(request.prompt)
    return response
