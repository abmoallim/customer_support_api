from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SupportRequest(BaseModel):
    prompt: str
    chat_history: List[object] = []

# Configure the OpenAI API
# openai.api_key = os.getenv("API_KEY")
client = openai.OpenAI(api_key=os.getenv("API_KEY"))

def read_company_info():
    """Read company information from data.txt file."""
    with open("data.txt", "r") as file:
        return file.read()
    
async def send_request_to_openai(prompt: str, chat_history: list[object]):
    """Generate a response using the OpenAI GPT-4 model with streaming."""
    company_info = read_company_info()
    
    system_message = f"""You are the best customer support AI. Use the following company information to assist customers:

    {company_info}

    If you cannot provide an appropriate answer, inform the customer that you cannot provide that feedback at the moment and offer to transfer them to a human agent.

    You can understand the Somali language. If the customer asks a question in Somali, you should respond in Somali. Although the company data is in English, you can translate your responses into Somali where necessary.
    If the customer asks a question that is not related to the company, you should respond with "I'm sorry, I can only assist with questions related to the company."
    If the customer speaks in Somali, you should respond in Somali Only without adding English.
    """

    messages = [ 
        {"role": "system", "content": system_message},
    ]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": prompt})
        
    
    response = client.chat.completions.create(
            model="gpt-4-0613",

            messages=messages,
        )
    return {
        "response": response.choices[0].message.content,
    }

@app.post("/api/v1/customer-support")
async def customer_support(request: SupportRequest):
    """Endpoint to handle customer support requests."""
    try:
        return await send_request_to_openai(request.prompt, request.chat_history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
