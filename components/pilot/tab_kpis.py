import os
import json
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_kpi

def render(kpi_ids):
    st.markdown("## 📊 KPIs Overview")

    # Load all KPI data
    all_kpis = load_kpi()

    # Filter based on stringified IDs
    filtered_kpis = [kpi for kpi in all_kpis if str(kpi["id"]) in kpi_ids]

    if not filtered_kpis:
        st.warning("No KPIs found for the selected IDs.")
        return

    # Map name to full data
    kpi_options = {kpi["name"]: kpi for kpi in filtered_kpis}

    # User selects KPI by name
    selected_name = st.selectbox("🎯 Select a KPI", list(kpi_options.keys()))
    selected_kpi = kpi_options[selected_name]

    # Dummy data for visualization
    dummy_data = pd.DataFrame({
        "Month": pd.date_range("2024-01-01", periods=6, freq="M"),
        "Value": [10, 15, 22, 18, 25, 30]
    })

    # Prepare values
    kpi_title = selected_kpi["name"]
    kpi_description = selected_kpi.get("indicator", "No description available.")
    kpi_unit = selected_kpi.get("unit", "")

    # Plot with description inside the plot area
    fig = px.line(
        dummy_data,
        x="Month",
        y="Value",
        labels={"Value": kpi_unit, "Month": "Month"},
        title=kpi_title
    )

    # Add description as annotation inside the plot
    fig.add_annotation(
        text=f"<b>Description:</b> {kpi_description}",
        xref="paper", yref="paper",
        x=0, y=1.05,
        showarrow=False,
        align="left",
        bordercolor="gray",
        borderwidth=1,
        bgcolor="white",
        opacity=0.9
    )

    st.plotly_chart(fig, use_container_width=True)
