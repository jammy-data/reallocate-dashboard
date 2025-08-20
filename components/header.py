import streamlit as st

def render():
    pages = {"Homepage": "pages/1_home.py", #"Barcelona Kepler": "pages/old/Barcelona deckgl.py",
}
    for col, (name, path) in zip(st.columns(len(pages)), pages.items()):
        col.page_link(path, label=name)