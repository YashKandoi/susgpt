import streamlit as st

def add(uploaded_file):
    pass
st.set_page_config(
    page_title="Add Data",
    page_icon="➕",
    #layout="wide",
    #initial_sidebar_state="expanded",
)
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    st.button("Upload", type="primary",on_click=add(uploaded_file))
