import re
from Retrieval import search_text
import config
import os
from openai import OpenAI
import pandas as pd

# 1. LOAD MODEL LLM
# model để sinh câu trả lời
def llm_chat(input):
    openai = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))
    response = openai.chat.completions.create(
                messages = input, # list hội thoại = lịch sử
                model = "gpt-4o-mini", # model llm openai
                temperature = 0.6, # độ sáng tạo 0.0->1.0
                stream = False
            )
    return response.choices[0].message.content

# model với các nhiệm vụ cụ thể như trích xuất
def llm_gen(input):
    openai = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))
    response = openai.chat.completions.create(
                messages = input,
                model = "gpt-4o-mini",
                temperature = 0.3,
                stream = False
            )
    return response.choices[0].message.content

# Xử lý lịch sử chat và thêm SYSTEM PROMPT
def process_chatbot_history(question, chatbot_history):

    # đọc dữ liệu từ file excel
    df = pd.read_excel('data/data_information.xlsx') #[0]
    for index, row in df.iterrows():
        data = row
        break
    # SYSTEM PROMPT
    start_history = [{'role': 'system', 'content': config.SYSTEM_PROMPT.format(time = data["time"], 
                                                                      total_money = data["total_money"],
                                                                      bill_image = data["bill_image"],
                                                                      app= data["app"],
                                                                      name= data["name"],
                                                                      birthday= data["birthday"],
                                                                      cccd= data["cccd"],
                                                                      cccd_image= data["cccd_image"],
                                                                      # các ví dụ hội thoại
                                                                      example = search_text(question, config.VECTOR_STORE['collection_name'])
                                                                      )}]
    # print(start_history)
    # print(chatbot_history)
    # cắt lịch sử chat với  giới hạn LEN_CHAT_HISTORY
    if len(chatbot_history) > config.LEN_CHAT_HISTORY:
        return start_history+ chatbot_history[config.LEN_CHAT_HISTORY: -1]
    else:
        # print(start_history+ chatbot_history)
        return start_history+ chatbot_history



# trích xuất tên ảnh
def extract_image(response):
    pattern = r'\"(.*?)*\"' # "ảnh bill.jpg"
    json_match = re.search(pattern, response, re.DOTALL)
    if json_match != None:
        content_json = json_match.group(0)
        image_name = re.sub(r"\"", "", content_json)
        # sửa lại phản hồi (bỏ câu văn về ảnh) => response: "em gửi bill ạ" 
        input = [{"role": "user", "content": config.EXTRACT_IMAGE_PROMPT.format(response=response)}]
        new_response = llm_gen(input) 
    else:
        image_name = ""
        new_response = response
    print("image_name", image_name)  
    print("new_response", new_response)  

    return image_name, new_response

# TẠO PHẢN HỒI VÀ TÊN ẢNH
def generate_llm(question, chat_history):
    input = {"role": "user", "content": question}
    chatbot_history = process_chatbot_history(question, chat_history) # system+ history
    chatbot_history.append(input)
    # print("chatbot_history", chatbot_history)
    response = llm_chat(chatbot_history)
    image_name, new_response = extract_image(response)
    return image_name, new_response

# Trích xuất thông tin của user
def extract_information(chatbot_history):
    # assistant_history= []
    # for data in chatbot_history:
    #     print("data", type(data))
    #     if data.role =="assistant":
    #         assistant_history.append(data)
    
    input = [{"role": "user", "content": config.EXTRACT_PROMPT.format(chat_history=chatbot_history)}]
    response = llm_gen(input)
    pattern = r'```json\s*(.*?)\s*```'  # ```json
                                        #   {
                                        # "Họ tên": "Trần Ngọc",
                                        # } 
                                        # ```
    json_match = re.search(pattern, response, re.DOTALL)
    content_json = json_match.group(1)
    return content_json