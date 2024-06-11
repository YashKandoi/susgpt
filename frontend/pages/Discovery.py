import streamlit as st
import time
import json
import requests

st.set_page_config(
    page_title="Chat",
    page_icon="🧊",
    #layout="wide",
    initial_sidebar_state="expanded",
)

url = 'http://127.0.0.1:8000/susgpt/discovery/'


def add_title():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
add_title()
st.title("SusGPT: Discovery Mode")
st.markdown("Find information about SusMafia Startups")
st.sidebar.title("SusGPT")

def getresponse(prompt):
    x = requests.post(url, data = {"question":prompt}).text.replace("\n","\\n").split('"response":')[1][2:-2].strip()
    return x


# Initialize chat history
if not st.session_state:
    st.session_state = []

# Display chat messages from history on app rerun
for message in st.session_state:
    print(message)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What does Smart Joules do?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.append({"role": "user", "content": prompt})
    response=""
    with st.spinner("Waiting"):
        response = getresponse(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.append({"role": "assistant", "content": response})
