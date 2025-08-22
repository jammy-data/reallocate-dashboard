import streamlit as st
import pandas as pd
import re

def render_pilot_card(row):
    """Render a single pilot card from a dataframe row."""
    intervention_start = row['Start Date']
    intervention_end = row['End Date']
    start_date = pd.to_datetime(intervention_start)
    end_date = pd.to_datetime(intervention_end)

    with st.expander(f"{row['name']}"):
        # Clean city name
        cleaned_city_name = re.sub(r'\(.*?\)', '', row['name']).strip()

        # Basic info
        st.write(f"📍 **City:** {cleaned_city_name}") 
        st.write(f"📅 **Start Date:** {start_date.date()}")
        st.write(f"📅 **End Date:** {end_date.date()}")

        # Extra info
        st.write(f"📝 **Description:** {row['Description']}")
        st.write(f"💡 **Lessons Learned:** {row['Lessons Learned']}")

        # Image (HTML to preserve style)
        if row["Pictures"]:
            st.markdown(
                f"""<img src="{row["Pictures"]}" alt="Image of {row['name']}" 
                width="300" class="city-image" />""",
                unsafe_allow_html=True,
            )

        # Navigation button
        link = f"pilot?pilot={row['id']}"
        st.markdown(
            f"""
            <a href="{link}" target="_self">
                <button style="margin-top: 1rem;">Show more</button>
            </a>
            """,
            unsafe_allow_html=True,
        )
