from qdrant_client import QdrantClient, models
import json
import streamlit as st
from utils import embed_text, load_embedding_model, preprocess_text
import datetime
import config

def search_text(text_query, collection_name):

    client = QdrantClient(url="http://localhost:6333")
    tokenizer, model = load_embedding_model()

    search_result=client.search(

        collection_name=collection_name,

        query_vector= embed_text(preprocess_text(text_query), tokenizer, model),

        limit=config.RETRIEVAL['top_k'],

        search_params=models.SearchParams(
                exact=True,  # Turns on the exact search mode KNN
            ),
   )

    
    answer_array=[]
    
    for i in search_result:
        answer_array.append(i.payload) 

    print(answer_array)
    return answer_array



# if __name__ == '__main__':

#     start_time = datetime.datetime.now()
  
#     print(search_text("ok vậy em gửi bill anh kiểm tra nhé", config.VECTOR_STORE['collection_name']))
#     # Kết thúc đo thời gian
#     end_time = datetime.datetime.now()
#     # Tính toán thời gian thực thi
#     elapsed_time = end_time - start_time
#     # Tính giờ, phút, giây
#     hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
#     minutes, seconds = divmod(remainder, 60)

#     print(f"Thời gian chạy: {int(hours)} giờ {int(minutes)} phút {seconds:.2f} giây")  