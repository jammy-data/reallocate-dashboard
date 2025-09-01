# app.py
import subprocess
import time
import requests
import streamlit as st
from streamlit import Page
from utils.config import LOGOS_DIR, PAGES_DIR
# --- Set favicon and page layout ---
st.set_page_config(
    page_title="REALLOCATE Dashboard",
    page_icon=str(LOGOS_DIR / "REALLOCATE-favicon.png"), # your project logo here
    layout="wide"
)
# --- Backend auto-start ---
BACKEND_URL = "http://127.0.0.1:8000/pilot_api_data?site_name=test"

def start_backend():
    try:
        # Try pinging backend
        requests.get(BACKEND_URL, timeout=2)
        # st.info("Backend already running.")
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        # Start backend in the background
        st.info("Starting backend server...")
        subprocess.Popen(["python", "backend.py"])
        time.sleep(5)  # wait a few seconds for backend to initialize

start_backend()

# --- Streamlit pages ---

home = Page(PAGES_DIR/"1_home.py", title="Home", )
pilot = Page(PAGES_DIR/"2_pilot.py", title="Pilot")

pg = st.navigation(
    {
        "Home": [home],
        "Pilot": [pilot]
    },
    position="hidden"  # or "sidebar"
)

pg.run()
