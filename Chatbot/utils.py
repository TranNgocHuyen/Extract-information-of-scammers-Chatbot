import re
from pyvi.ViTokenizer import tokenize
import torch
from transformers import AutoModel, AutoTokenizer

import config
import streamlit as st

def clean_text(text):

    # # xóa dấu câu, kí tự đặc biệt
    text = re.sub(r'[\+\-\–\|\:\(\)\"\/\>\:\…]', ' ', text)
    text = text.replace("...", " ")\
                .replace('\n', '.')\
                .replace('\xa0', '')
    
    # Xóa các dấu . liên tiếp
    text = re.sub(r'\.+', '.', text)

    # xóa khoảng trắng liên tiếp
    text = ' '.join(text.split())
    
    # Chuyển về in thường
    return text.lower() 

def preprocess_text(text):
    text = clean_text(text)
    
    # pyvi
    text = tokenize(text)
    
    # xóa khoảng trắng liên tiếp
    return ' '.join(text.split())

# @st.cache_resource
def load_embedding_model():
    checkpoint_model = config.EMBEDDING_MODEL['model_name'] 
    tokenizer = AutoTokenizer.from_pretrained(checkpoint_model) 
    model = AutoModel.from_pretrained(checkpoint_model)
    # print(tokenizer)
    # print(model)
    return tokenizer, model


# Load model and embedding text funtion
def embed_text(text, tokenizer, model):
    text = preprocess_text(text)
    inputs = tokenizer(text,padding=True, truncation=True, return_tensors="pt") #258
    
    #print(f"Token sau khi tokenizer: {tokenizer.tokenize(text)}",'==')
    print(f"Chiều dài token: {len(tokenizer.tokenize(text))}",'===')

    with torch.no_grad():
        embeddings = model(**inputs, output_hidden_states=True, return_dict=True).pooler_output

    return embeddings.numpy()[0].tolist()
            #torch.Tensor [1, 768] =>numpy.ndarray (1, 768)=> (768,) => list

