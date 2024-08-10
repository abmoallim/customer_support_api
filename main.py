from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os
from dotenv import load_dotenv
import google.generativeai as genai

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

# Configure the Google Gemini API
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro-exp-0801')

def read_company_info():
    """Read company information from data.txt file."""
    with open("data.txt", "r") as file:
        return file.read()

async def send_request_to_gemini(prompt: str):
    """Generate a response using the Gemini model with streaming."""
    company_info = read_company_info()
    
    system_message = f"""You are the best customer support AI. Use the following company information to assist customers:

{company_info}

If you cannot provide an appropriate answer, inform the customer that you cannot provide that feedback at the moment and offer to transfer them to a human agent.

You can understand the Somali language. If the customer asks a question in Somali, you should respond in Somali. Although the company data is in English, you can translate your responses into Somali where necessary.
If the customer asks a question that is not related to the company, you should respond with "I'm sorry, I can only assist with questions related to the company."
if the customer speakes in Somali, you should respond in Somali Only with out you adding engish.
"""

    user_message = prompt
    message = f"{system_message}\n\nCustomer: {user_message}\n\nAI:"

    response = model.generate_content(message, stream=True)

    async def generate():
        for chunk in response:
            yield f"data: {chunk.text}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/api/v1/customer-support")
async def customer_support(request: SupportRequest):
    """Endpoint to handle customer support requests."""
    try:
        return await send_request_to_gemini(request.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
