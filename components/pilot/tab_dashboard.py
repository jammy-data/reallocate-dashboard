import streamlit as st

def render(dash):
    if dash["title"] == "":
        st.error("No dashboard has been created")
        return  # ⬅️ stops only this function, not the whole page
    
    st.title(dash.get('title', 'Dashboard Info'))
    st.write(dash.get("description", "Lorem Ipsum\nDolor sit amet, consectetur adipiscing elit.\nSed do eiusmod tempor incididunt ut labore et dolore magna aliqua."))

    for selector in dash.get("selectors", []):
        st.selectbox(f"Select {selector}", ["Option A", "Option B"])  # Dummy
