import streamlit as st
from utils.config import COMPONENTS_DIR

def render_styles():
    """
    Include custom CSS styles in the app.
    """
    with open(COMPONENTS_DIR / "styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
