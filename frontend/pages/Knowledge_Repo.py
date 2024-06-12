import streamlit as st
import requests

def initialize():
    requests.post("http://127.0.0.1:8000/susgpt/clearPdfFolder/")
    files = {'pdf_file': (uploaded_file.name, uploaded_file.getvalue(), 'multipart/form-data')}
    requests.post("http://127.0.0.1:8000/susgpt/initializeKnowledgeRepo/",files=files)

st.set_page_config(
    page_title="Knowledge Repo",
    page_icon="📚",
    #layout="wide",
    initial_sidebar_state="expanded",
)

st.title("SusGPT: Knowledge Repo Mode")
st.markdown("Add Data to the Database of SusGPT and Use It")
st.sidebar.title("SusGPT")

url="http://127.0.0.1:8000/susgpt/knowledgeRepoChatbot/"

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

uploaded_file = st.file_uploader("Choose a pdf file:",type=['pdf'])
with st.spinner("Waiting"):
    pressed=st.button("Upload",on_click=initialize)


# React to user input
if prompt := st.chat_input("What are the jobs in Climate Change Sector in India?"):
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
