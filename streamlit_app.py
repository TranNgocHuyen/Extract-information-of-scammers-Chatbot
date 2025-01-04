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
    
    if "chatbot_history" not in st.session_state:
        data = st.session_state.data_infor
        st.session_state.chatbot_history = [
            {'role': 'assistant', 'content': "Chào anh, anh hỗ trợ thu hồi vốn treo phải không ạ? Anh tư vấn cho em với."}
        ]
    # st.session_state.chatbot_history
    def stream_llm_response(response):
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    # Hiển thị conversation
    for i, message in enumerate(st.session_state.chatbot_history):
        if len(st.session_state.chatbot_history) <2:
            with st.chat_message(message['role']):
                    st.markdown(message['content'])
        else:
            if i>0:
                with st.chat_message(message['role']):
                    st.markdown(message['content'])

    if prompt:= st.chat_input("Say something ..."):
        with st.chat_message('user'):
            st.markdown(prompt)
        with st.chat_message('assistant'):

            # response = generate(prompt,st.session_state.chatbot_history) # , st.session_state.chatbot_history
            image, response = generate_llm(prompt,st.session_state.chatbot_history)
            
            st_response = st.write(response)
        if image != "":
            with st.chat_message('assistant'):
                st.image("data/image/"+ image)
        
        st.session_state.chatbot_history.append({"role": "user", "content": prompt}) 
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

    # if os.path.exists('data_trich_xuat.csv') :
    #     df = pd.read_csv('data_trich_xuat.csv')
    #     df.loc[len(df)] = data[0]
    #     df.to_csv('data_trich_xuat.csv', sep= '\t', header = True,)
    # else:
    #     df1.to_csv('data_trich_xuat.csv', sep= '\t', header = True,)