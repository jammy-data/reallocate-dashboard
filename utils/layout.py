import streamlit as st
from utils.data_loader import load_logos

LOGOS = load_logos()

def show_logo_image():
    st.image("assets/images/reallocate_logo.png", width=200)

def show_separator():
    st.markdown("---")

def show_logos_from_list(logos=LOGOS):  # Default to the global LOGOS
    css = """
    <style>
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        margin: 20px 0;
    }
    .image-container img {
        max-height: 80px;
        max-width: 150px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    html = f"""<div class="image-container">
                    <img src="{LOGOS["reallocate"]["src"]}"></a>
                    <img src="{LOGOS["bsc"]["src"]}"></a>
                    <img src="{LOGOS["iti"]["src"]}"></a>
                </div>
    """
    st.markdown(html, unsafe_allow_html=True)

