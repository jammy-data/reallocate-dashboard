# app.py
import streamlit as st
st.set_page_config(layout="wide")  # FIRST line!

from streamlit import Page
home = Page("pages/1_home.py", title="Home", icon="🏠")
pilot = Page("pages/2_pilot.py", title="Pilot", icon="👨‍✈️")

pg = st.navigation(
    {
        "Home": [home],
        "Pilot": [pilot]
    },
    position="hidden"  # or "sidebar"
)

pg.run()
