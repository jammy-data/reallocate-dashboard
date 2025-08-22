import folium
from folium.elements import MacroElement
from jinja2 import Template
import requests
import json
import base64
import streamlit as st
from streamlit_folium import st_folium
from utils.helper_functions import value_to_color, average_color, get_binary_file, get_api_url, reset_filters

from utils.config import PILOTS_DIR,MAPS_DIR


def render_pilot_map(df, indicators, legend_template, col1, col2):
    """
    Render a map with circle markers for each pilot in the dataframe.

    Args:
        df (pd.DataFrame): Dataframe with pilot data including lat, lon, and name.
        indicators (dict): Mapping of SUMI indicators.
        legend_template (str): Folium legend template (HTML).
        col1 (st.column), col2 (st.column): Streamlit columns for layout.
    """
    with col2:
        # Initialize the map (centered on Europe)
        m = folium.Map(location=[50, 10], zoom_start=4)

        # Add legend
        macro = MacroElement()
        macro._template = Template(legend_template)
        m.get_root().add_child(macro)

        # Iterate over pilots
        for _, row in df.iterrows():
            lat, lon = row['lat'], row['lon']
            site_name = row['name']

            # Load dummy indicator data
            with open(PILOTS_DIR/"pilot_indicators_dummy.json") as f1:
                indicator_data = json.load(f1)

            # Determine color
            if st.session_state.selected_sumi:
                sumi_indicators = indicators.get(st.session_state.selected_sumi, [])
                color_list = []
                for indicator in sumi_indicators:
                    key = indicator.lower().replace(" ", "_")
                    indicator_values = indicator_data.get(key)  # get the indicator data
                    if indicator_values is not None:
                        color_list.append(value_to_color(indicator_values))
                    else:
                        # fallback color if data is missing
                        color_list.append("rgb(128, 128, 128)")
                current_color = average_color(color_list)
                current_color = average_color(color_list)
                map_file = MAPS_DIR/f"{st.session_state.selected_sumi}_map.html"
            elif st.session_state.kpi.lower().replace(" ", "_") in indicator_data:
                key = st.session_state.kpi.lower().replace(" ", "_")
                current_color = value_to_color(indicator_data[key])
                map_file = MAPS_DIR / f"{key}_map.html"
            else:
                current_color = "rgb(128, 128, 128)"  # grey
                map_file = MAPS_DIR /f"{st.session_state.kpi.lower().replace(' ', '_')}_map.html"

            # Fetch external API data
            try:
                api_url = get_api_url()
                response = requests.get(api_url, params={"site_name": site_name})
                response.raise_for_status()
                data = response.json()

                weather = data[site_name].get("weather", {})
                aqi = data[site_name].get("air_quality", {}).get("AQI", "N/A")
                traffic = data[site_name].get("traffic", {}).get("congestion_level", "N/A")

                temperature = weather.get("temperature", "N/A")
                humidity = weather.get("humidity", "N/A")
                precipitation = weather.get("precipitation", "N/A")

                popup_string = f"""
                <b>{site_name}</b><br>
                🌡️&nbsp;{temperature}°C&nbsp;&nbsp;
                💧&nbsp;{humidity}%&nbsp;&nbsp;
                ☔&nbsp;{precipitation}mm&nbsp;&nbsp;
                🍃&nbsp;{round(((500 - aqi) / 500) * 100)}%&nbsp;&nbsp;
                🚗&nbsp;{round(traffic * 100)}%&nbsp;
                """
            except requests.exceptions.RequestException as e:
                popup_string = f"<b>{site_name}</b><br>Error fetching data: {e}"

            # Add circle marker
            folium.CircleMarker(
                location=[lat, lon],
                radius=8,
                popup=popup_string,
                color=current_color,
                fill=True,
                fill_color=current_color,
                fill_opacity=0.6
            ).add_to(m)

        # Save map
        m.save(map_file)

        # Encode to base64 for download
        map_data = get_binary_file(map_file)
        b64_map = base64.b64encode(map_data).decode()

        # Download button in col1
        with col1:
            st.write("\n\n\n")
            st.download_button(
                label="📥 Download Map",
                data=map_data,
                file_name=map_file.name,  # <- Use .name instead of replace()
                mime="text/html"
            )
            st.button("🔄 Remove Filters", key="reset-button", type="secondary", on_click=reset_filters)

        # Display map
        st_folium(m, width="100%", height=600, key="map_initial_load")

    return m
