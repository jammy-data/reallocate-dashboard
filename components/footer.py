import streamlit as st
from utils.layout import  show_logos_from_list
def render():
    st.write("---")
    show_logos_from_list()  # Uses default LOGOS from layout    
    st.write("---")
