import streamlit as st
import json
import pandas as pd
from utils.helper_functions import get_base64_image, filter_pilots_by_category, load_html
from utils.config import COMPONENTS_DIR, CONFIG_DIR, LOGOS_DIR
from components.home import (
    header,
    footer,
    styles,
    scripts,
    controls_panel,
    impact_buttons,
    pilot_map,
    pilot_card,
    kpi_selector
)

# --- Load data ---
pilots_static_df = pd.read_json(CONFIG_DIR / 'pilot_static_data.json')
legend_template = load_html(COMPONENTS_DIR / "legend_macro.html")

with open(CONFIG_DIR / "indicators.json") as f_ind:
    indicators = json.load(f_ind)

indicator_list = [item for sublist in indicators.values() for item in sublist if item != ""]

# --- Session state defaults ---
if "kpi" not in st.session_state:
    st.session_state.kpi = indicator_list[0]
    st.session_state.legend = st.session_state.kpi
if "selected_sumi" not in st.session_state:
    st.session_state.selected_sumi = None
if "impact_area" not in st.session_state:
    st.session_state.impact_area = None
if "filtered_pilots_df" not in st.session_state:
    st.session_state.filtered_pilots_df = pilots_static_df

# --- Callbacks ---
def reset_sumi():
    st.session_state.legend = st.session_state.kpi
    st.session_state.selected_sumi = None

def reset_impact_area():
    st.session_state.impact_area = None

def update_pilots():
    if st.session_state.impact_area:
        st.session_state.filtered_pilots_df = filter_pilots_by_category(
            pilots_static_df, st.session_state.impact_area
        )
    elif st.session_state.selected_sumi:
        st.session_state.filtered_pilots_df = filter_pilots_by_category(
            pilots_static_df, st.session_state.selected_sumi
        )
    else:
        st.session_state.filtered_pilots_df = pilots_static_df

def update_impact_area(area):
    st.session_state.impact_area = area
    reset_sumi()
    update_pilots()

# --- Load logos ---
logo1_base64 = get_base64_image(LOGOS_DIR / "logo.jpg")
logo2_base64 = get_base64_image(LOGOS_DIR / "REALLOCATE_Logo.png")

# --- Render components ---
styles.render_styles()
scripts.render_scripts()
header.render_header(st.session_state.legend, logo1_base64, logo2_base64)

# --- Layout: left controls / right map ---
col1, col2 = st.columns([1.75, 4])
controls_panel.render_controls(col1, indicators, update_pilots)
impact_buttons.render_impact_buttons(update_impact_area)

pilot_map.render_pilot_map(
    df=st.session_state.filtered_pilots_df,
    indicators=indicators,
    legend_template=legend_template,
    col1=col1,
    col2=col2
)

kpi_selector.render_kpi_selector(indicator_list, on_change_callback=reset_sumi)

# --- Pilots cards ---
st.markdown('<h1 class="custom-title1">Pilots</h1>', unsafe_allow_html=True)
for _, row in st.session_state.filtered_pilots_df.iterrows():
    pilot_card.render_pilot_card(row)

# --- Footer ---
footer.render_footer(logo1_base64, logo2_base64)
