import streamlit as st
from utils.helper_functions import get_base64_image
from utils.config import IMAGES_DIR

def render_impact_buttons(update_impact_area):
    """
    Render four impact area buttons with images in columns.

    Args:
        update_impact_area (callable): Function to call when a button is clicked.
    """
    # Load images and convert to base64
    image_paths = ["road_safety.png", "environment.png", "governance.png", "accessibility.png"]
    image_base64 = [get_base64_image(IMAGES_DIR / img) for img in image_paths]

    # Define impact areas
    impact_areas = ["Road Safety", "Environmental", "Transformative Governance", "Inclusivity/Accessibility"]

    # Create layout columns
    empty_col1, col1, col2, col3, col4, empty_col2 = st.columns([1, 2, 2, 2, 2, 1])

    for idx, col in enumerate([col1, col2, col3, col4]):
        with col:
            # Render image above button
            button_html = f"""
            <div class="image-button">
                <img src="{image_base64[idx]}" alt="{impact_areas[idx]}">
            </div>
            """
            st.markdown(button_html, unsafe_allow_html=True)

            # Render the button
            if st.button(f"{impact_areas[idx]}", key=f"{impact_areas[idx]}", type="primary"):
                update_impact_area(impact_areas[idx])
