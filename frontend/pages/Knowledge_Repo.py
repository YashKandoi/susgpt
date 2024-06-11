import streamlit as st
import requests

def initialize():
    requests.post("http://127.0.0.1:8000/susgpt/clearPdfFolder/")
    requests.post("http://127.0.0.1:8000/susgpt/initializeKnowledgeRepo/",data={"pdf_file":uploaded_file.getvalue()})

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

def getresponse(prompt,role,skills):
    x = requests.post(url, data = {"question":prompt,"skills":skills,"role":role}).text.replace("\n","\\n").split('"response":')[1][2:-2].strip()
    return x


# Initialize chat history
if not st.session_state:
    st.session_state = []

# Display chat messages from history on app rerun
for message in st.session_state:
    print(message)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

uploaded_file = st.file_uploader("Choose a file")
pressed=st.button("Upload",on_click=initialize)

if uploaded_file is not None and pressed:

    # React to user input
    if prompt := st.chat_input("What are the jobs in Climate Change Sector in India?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.append({"role": "user", "content": prompt})
        response=""
        with st.spinner("Waiting"):
            response = getresponse(prompt,role,skills)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.append({"role": "assistant", "content": response})
