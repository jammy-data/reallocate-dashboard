import streamlit as st
from utils.helper_functions import get_base64_image
from utils.config import IMAGES_DIR

def render_impact_buttons(update_impact_area):
    """
    Render four impact area buttons with images in evenly spaced columns.

    Args:
        update_impact_area (callable): Function to call when a button is clicked.
    """
    # Load images and convert to base64
    image_paths = ["road_safety.png", "environment.png", "governance.png", "accessibility.png"]
    image_base64 = [get_base64_image(IMAGES_DIR / img) for img in image_paths]

    # Define impact areas
    impact_areas = ["Road Safety", "Environmental", "Transformative Governance", "Inclusivity/Accessibility"]

    # Create columns dynamically with padding on the sides
    num_buttons = len(impact_areas)
    cols = st.columns([1] + [2]*num_buttons + [1])  # first and last are empty padding columns
    button_cols = cols[1:-1]  # skip padding columns

    for idx, col in enumerate(button_cols):
        with col:
            # Render image above button
            st.markdown(
                f'<div class="image-button"><img src="{image_base64[idx]}" alt="{impact_areas[idx]}"></div>',
                unsafe_allow_html=True
            )
            # Render the button
            if st.button(impact_areas[idx], key=impact_areas[idx], type="primary"):
                update_impact_area(impact_areas[idx])
