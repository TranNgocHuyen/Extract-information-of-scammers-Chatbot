from typing import Union, List
from fastapi import FastAPI, Body
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from Generation import extract_information, generate_llm

# FAST API 
origins = ["*"]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    prompt: str
    history: List[Message]

class ExtractRequest(BaseModel):
    history: List[Message]

@app.post("/chat")
def post_message(request: ChatRequest):
    image_name, response = generate_llm(request.prompt, request.history) # hàm xử lý: generate_llm
    print(image_name)
    print(response)
    return {"response": {"role": "assistant", "content": response},
            "image_name": image_name}

@app.post("/data")
def get_extracted_information(request: ExtractRequest):
    return {"data": extract_information(request.history)} # hàm xử lý : extract_information
