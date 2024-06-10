import streamlit as st

st.set_page_config(
    page_title="Chat",
    page_icon="🧊",
    #layout="wide",
    #initial_sidebar_state="expanded",
)
st.title("SusGPT")
st.sidebar.title("SusGPT")

def getresponse(prompt):
    return "hi"


# Initialize chat history
if not st.session_state:
    st.session_state = []

# Display chat messages from history on app rerun
for message in st.session_state:
    print(message)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.append({"role": "user", "content": prompt})

    response = f"{getresponse(prompt)}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.append({"role": "assistant", "content": response})
