import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
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
st.title("SusGPT")
st.sidebar.title("SusGPT")

st.markdown("SusGPT is a sustainability chatbot. Select options from the sidebar to continue :)")
