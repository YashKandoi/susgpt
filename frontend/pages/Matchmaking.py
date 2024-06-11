import streamlit as st
import requests

def add(uploaded_file):
    pass
st.set_page_config(
    page_title="Matchmaking",
    page_icon="➕",
    #layout="wide",
    #initial_sidebar_state="expanded",
)

def add_title():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "SusGPT";
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

url="http://127.0.0.1:8000/susgpt/matchmaking/"

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

role = st.selectbox("Select your role: ",["Software Engineer", "Product Manager"])
skills = st.text_input("Enter your skills: ",placeholder="Python, SQL, Machine Learning")

# React to user input
if prompt := st.chat_input("What is up?"):
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
