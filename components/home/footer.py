import streamlit as st

def render_footer(logo1_base64, logo2_base64):
    """
    Render the app footer with logos and copyright.
    """
    st.markdown(
        f"""
        <div class="footer-container">
            <div class="footer-text">
                © 2025 CERTH-ITI. All rights reserved.
            </div>
            <div class="footer-logos">
                <img src="data:image/jpeg;base64,{logo1_base64}" class="footer-logo" alt="ITI logo" />
                <img src="data:image/png;base64,{logo2_base64}" class="footer-logo" alt="REALLOCATE logo" />
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
