import streamlit as st
import pandas as pd
import json
import os
import config
from Generation import extract_information, generate, generate_llm
import pandas as pd
tab1, tab2 = st.tabs(["Chatbot", "Data"])
with tab1:
    # Khởi tạo lưu trữ chatbot_history
    if "data_infor" not in st.session_state:
        df = pd.read_excel('data/data_information.xlsx') #[0]
        for index, row in df.iterrows():
            st.session_state.data_infor = row
            break
    st.session_state.chatbot_history
    if "chatbot_history" not in st.session_state:
        data = st.session_state.data_infor
        st.session_state.chatbot_history = [
            {'role': 'system', 'content': config.SYSTEM_PROMPT.format(time = data["time"], 
                                                                      total_money = data["total_money"],
                                                                      bill_image = data["bill_image"],
                                                                      app= data["app"],
                                                                      name= data["name"],
                                                                      birthday= data["birthday"],
                                                                      cccd= data["cccd"],
                                                                      cccd_image= data["cccd_image"],
                                                                      )},
            {'role': 'assistant', 'content': "Chào anh, anh hỗ trợ thu hồi vốn treo phải không ạ? Anh tư vấn cho em với."}
        ]
    def stream_llm_response(response):
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    # Hiển thị conversation
    for i, message in enumerate(st.session_state.chatbot_history):
        if i>=0:
            with st.chat_message(message['role']):
                st.markdown(message['content'])

    if prompt:= st.chat_input("Say something ..."):
        with st.chat_message('user'):
            st.markdown(prompt)
        with st.chat_message('assistant'):

            # response = generate(prompt,st.session_state.chatbot_history) # , st.session_state.chatbot_history
            image, response = generate_llm(prompt,st.session_state.chatbot_history)
            
            response = st.write_stream(stream_llm_response(response))  
            print(image)
        with st.chat_message('assistant'):
            st.image("data/image/"+ image)
        
        st.session_state.chatbot_history[-1]= {"role": "user", "content": prompt}
        st.session_state.chatbot_history.append({'role': 'assistant', 'content': response})

with tab2:
    information = extract_information(st.session_state.chatbot_history)
    information = json.loads(information)

    data = [[value for _, value in information.items()]]

    df1 = pd.DataFrame(
        data,
        columns = [ key for key, _ in information.items()]
    )
    st.table(df1)
