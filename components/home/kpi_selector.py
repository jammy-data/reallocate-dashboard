import streamlit as st

def render_kpi_selector(indicator_list, on_change_callback):
    """
    Render a KPI selectbox.

    Args:
        indicator_list (list): List of available KPIs.
        on_change_callback (callable): Function to call when selection changes.
    """
    st.selectbox(
        "Select a KPI",
        indicator_list,
        key='kpi',
        on_change=on_change_callback
    )
