import re
from Retrieval import search_text
import config
import os
from openai import OpenAI
import pandas as pd

# 1. LOAD MODEL LLM
def llm_stream(input):
    openai = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))
    response = openai.chat.completions.create(
                messages = input,
                model = "gpt-4o-mini",
                temperature = 0.7,
                stream = True
            )
    return response

def llm(input):
    openai = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))
    response = openai.chat.completions.create(
                messages = input,
                model = "gpt-4o-mini",
                temperature = 0.2,
                stream = False
            )
    return response.choices[0].message.content

# Xử lý lịch sử chat
def process_chatbot_history(question, chatbot_history):
    df = pd.read_excel('data/data_information.xlsx') #[0]
    for index, row in df.iterrows():
        data = row
        break
    start_history = [{'role': 'system', 'content': config.SYSTEM_PROMPT.format(time = data["time"], 
                                                                      total_money = data["total_money"],
                                                                      bill_image = data["bill_image"],
                                                                      app= data["app"],
                                                                      name= data["name"],
                                                                      birthday= data["birthday"],
                                                                      cccd= data["cccd"],
                                                                      cccd_image= data["cccd_image"],
                                                                      example = search_text(question, config.VECTOR_STORE['collection_name'])
                                                                      )}]
    # print(start_history)
    # print(chatbot_history)
    if len(chatbot_history) > config.LEN_CHAT_HISTORY:
        return start_history+ chatbot_history[config.LEN_CHAT_HISTORY: -1]
    else:
        # print(start_history+ chatbot_history)
        return start_history+ chatbot_history
    


def generate(question, chat_history):
    input = {"role": "user", "content": question}
    chatbot_history = process_chatbot_history(chat_history)
    chatbot_history.append(input)
    response = llm_stream(chatbot_history)
    
    return response

def generate_llm(question, chat_history):
    input = {"role": "user", "content": question}
    chatbot_history = process_chatbot_history(question, chat_history)
    chatbot_history.append(input)
    # print("chatbot_history", chatbot_history)
    response = llm(chatbot_history)
    image_name, new_response = extract_image(response)
    return image_name, new_response


def extract_information(chatbot_history):
    input = [{"role": "user", "content": config.EXTRACT_PROMPT.format(chat_history=chatbot_history)}]
    response = llm(input)
    pattern = r'```json\s*(.*?)\s*```'
    json_match = re.search(pattern, response, re.DOTALL)
    content_json = json_match.group(1)
    return content_json

def extract_image(response):
    pattern = r'\"(.*?)*\"'
    json_match = re.search(pattern, response, re.DOTALL)
    if json_match != None:
        content_json = json_match.group(0)
        image_name = re.sub(r"\"", "", content_json)
        input = [{"role": "user", "content": config.EXTRACT_IMAGE_PROMPT.format(response=response)}]
        new_response = llm(input) 
    else:
        image_name = ""
        new_response = response
    print("image_name", image_name)  
    print("new_response", new_response)  

    return image_name, new_response