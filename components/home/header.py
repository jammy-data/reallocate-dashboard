import streamlit as st

def render_header(legend_title, logo1_base64, logo2_base64):
    """
    Render the app header with title, subtitle, and logos.

    Args:
        legend_title (str): Current KPI or SUMI legend.
        logo1_base64 (str): Base64 string for the first logo.
        logo2_base64 (str): Base64 string for the second logo.
    """
    st.markdown(
        f"""
        <div class="custom-container">
            <div class="header-container">
                <h1 class="custom-title1">Common Indicators</h1>
                <h2 class="custom-title2">{legend_title.replace("_", " ").title()}</h2>
            </div>
            <div class="logos-container">
                <img src="data:image/png;base64,{logo2_base64}" class="logo" alt="REALLOCATE logo" />
                <img src="data:image/jpeg;base64,{logo1_base64}" class="logo" alt="ITI logo" />
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
