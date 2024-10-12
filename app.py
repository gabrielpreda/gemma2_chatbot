
import streamlit as st
import os
from io import StringIO
import requests


st.set_page_config(page_title='Gemma2 Chatbot', 
                    page_icon = "images/gemma_avatar.jpg",
                    initial_sidebar_state = 'auto')

background_color = "#252740"

avatars = {
    "assistant" : "images/gemma_avatar.jpg",
    "user": "images/user_avatar.png"
}

st.markdown("<h2 style='text-align: center; color: #3184a0;'>Gemma2 Chatbot</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.image("images/gemma.jpg")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"], 
                         avatar=avatars[message["role"]]):
        st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]
    
st.sidebar.button("Clear Chat History", on_click=clear_chat_history)

def run_query(input_text):
    """
    """
    data={'input_text': input_text}
    r = requests.post('http://127.0.0.1:8000/chat_messages', json = data)

    
    if r.status_code == 200:
        print(r.content)
        agent_message = r.json()["agent"]

        return agent_message
    
    return "Error"

output = st.empty()
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=avatars["user"]):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant", avatar=avatars["assistant"]):
        with st.spinner("Thinking..."):
            

            response = run_query(prompt)

            placeholder = st.empty()
            full_response = ""
            for item in response:
                full_response += item
                placeholder.markdown(full_response, unsafe_allow_html=True)
            placeholder.markdown(response, unsafe_allow_html=True)

    message = {"role": "assistant", 
               "content": response,
               "avatar": avatars["assistant"]}
    st.session_state.messages.append(message)