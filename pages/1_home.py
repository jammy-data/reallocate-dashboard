import streamlit as st
from components import header,footer
from components.home import pilots
# from utils.helpers import slugify  # We'll create this next

header.render()

st.title("🧭 Pilot Projects Overview")

pilots.render()

footer.render()
