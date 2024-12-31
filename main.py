from typing import Union, List
from fastapi import FastAPI, Body
from pydantic import BaseModel

from Generation import extract_information, generate_llm
app = FastAPI()

class Message(BaseModel):
    role:str
    content: str

@app.post("/chat")
def post_message(prompt: Union[str, None] = None, history: List[Message]= Body(default=[])):
    image_name, response = generate_llm(prompt, history)
    print(image_name)
    print(response)
    return {"response" :
                {"role": "assistant", "content": response},
            "image_name":image_name }

@app.post("/data")
def get_extracted_information(history: List[Message]= Body(default=[])):
    return {"data": extract_information(history)}
