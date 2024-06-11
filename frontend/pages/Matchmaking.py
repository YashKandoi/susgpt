import streamlit as st

def add(uploaded_file):
    pass
st.set_page_config(
    page_title="Add Data",
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
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    st.button("Upload", type="primary",on_click=add(uploaded_file))
