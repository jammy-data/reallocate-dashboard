import streamlit as st
import time
import json
import folium
from streamlit_folium import st_folium
from datetime import datetime
# from visualization_utils import create_barplot, create_linechart
from branca.element import Template, MacroElement
from helper_functions import value_to_color, average_color, get_binary_file, load_html, get_base64_image
import streamlit.components.v1 as components
import random
import requests
import base64
import os

# Load the legend template as an HTML element
legend_template = load_html("./static/legend_macro.html")
def get_api_url():
    # Check if we're inside Docker (by checking the environment variable)
    if os.getenv('DOCKER', 'false') == 'true':
        return "http://host.docker.internal:8000/pilot_api_data"
    else:
        return "http://127.0.0.1:8000/pilot_api_data"

st.set_page_config(page_title="My App", layout="wide")  # Adjust layout to wide for more space

# Load JSON data
with open("./static/indicators.json") as f_ind:
    indicators = json.load(f_ind)

indicator_list = [item for sublist in indicators.values() for item in sublist]

with open("./pilot_sites.json") as f:
    pilots = json.load(f)

if "kpi" not in st.session_state:
    st.session_state.kpi = indicator_list[0]
    st.session_state.legend = st.session_state.kpi
if "selected_sumi" not in st.session_state:
    st.session_state["selected_sumi"] = None

# Define a callback function to reset `selected_sumi`
def reset_sumi():
    st.session_state.legend = st.session_state.kpi
    if st.session_state["selected_sumi"] is not None:
        st.session_state["selected_sumi"] = None

logo1_base64 = get_base64_image("./static/logo.jpg")
logo2_base64 = get_base64_image("./static/REALLOCATE_Logo.png")



# Title of the app
st.markdown(
    f"""
    <div class="custom-container">
        <!-- Title on the left side -->
        <div class="header-container">
            <h1 class="custom-title1">Common Indicators</h1>
            <h2 class=custom-title2>{st.session_state.legend.replace("_", " ").title()}</h2>
        </div>
        <div class="logos-container">
            <img src="data:image/png;base64,{logo2_base64}" class="logo" alt="REALLOCATE logo" />
            <img src="data:image/jpeg;base64,{logo1_base64}" class="logo" alt="ITI logo" />
        </div>
        </div>
    </div>
    """, unsafe_allow_html=True
)
# st.markdown(f'<h1 class="custom-title">Common Indicators: {st.session_state.legend.replace("_", " ").title()}</h1>', unsafe_allow_html=True)
# st.title(f"Common Indicators: {st.session_state.legend.replace('_', ' ').title()}")       

# Initialize a 2-column layout (left for controls, right for the map)
col1, col2 = st.columns([1, 3])  # Adjust the ratio as needed

# Left column (col1): Controls
with col1:
    # Update the selected KPI
    # st.write("Choose a KPI:")
    selected_kpi = st.selectbox("Choose a KPI or click a UMI:", indicator_list, key='kpi', on_change=reset_sumi)
    st.write("\n")
    # st.header("SUMI categories")
    # st.write("Or choose a SUMI:")
    def update_sumi(sumi):
        st.session_state["selected_sumi"] = sumi
        st.session_state.legend = sumi

    sumis = list(indicators.keys())
    for sumi in sumis:
        sumi_string = sumi.replace("_", " ").title()
        st.button(sumi_string, on_click=update_sumi, args=(sumi,))

# Right column (col2): Map
with col2:
    # Initialize the map with a default center (centered on Europe)
    m = folium.Map(location=[50, 10], zoom_start=4)

    macro = MacroElement()
    macro._template = Template(legend_template)
    m.get_root().add_child(macro)

    # Add circle markers for all cities with color configuration
    for site in pilots:
        lat = site["coordinates"][0]
        lon = site["coordinates"][1]
        site_name = site["name"]
        site_lower = site["name"].lower()  # Convert site to lowercase

        with open(f"./{site_lower}_indicators_dummy.json") as f1:
            indicator_data = json.load(f1)

        # Check the selected SUMI or KPI and set color
        if st.session_state.selected_sumi is not None:
            sumi_indicators = indicators[st.session_state.selected_sumi]
            color_list = []
            for indicator in sumi_indicators:
                if indicator.lower().replace(" ", "_") in indicator_data.keys():
                    indicator_values = indicator_data[indicator.lower().replace(" ", "_")]
                    color = value_to_color(indicator_values)
                else:
                    color = f"rgb(128, 128, 128)"  # grey
                color_list.append(color)
            current_color = average_color(color_list)
            map_file = "{}_map.html".format(st.session_state.selected_sumi)
        elif st.session_state.kpi.lower().replace(" ", "_") in indicator_data.keys():
            indicator_values = indicator_data[st.session_state.kpi.lower().replace(" ", "_")]
            current_color = value_to_color(indicator_values)
            map_file = "{}_map.html".format(st.session_state.kpi.lower().replace(" ", "_"))
        else:
            current_color = f"rgb(128, 128, 128)"  # grey
            map_file = "{}_map.html".format(st.session_state.kpi.lower().replace(" ", "_"))


        try:
            api_url = get_api_url()
            response = requests.get(api_url, params={"site_name": site_name})
            # response = requests.get("http://127.0.0.1:8000/pilot_api_data", params={"site_name": site_name})
            response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
            data = response.json()

            # print(data)
            # Extract weather, AQI, and traffic data
          
            temperature = data[site_name]['weather'].get("temperature", "N/A")
            humidity = data[site_name]['weather'].get("humidity", "N/A")
            precipitation = data[site_name]['weather'].get("precipitation", "N/A")
            aqi = data[site_name]['air_quality'].get("AQI", "N/A")  # Default to max AQI if missing
            traffic = data[site_name]['traffic'].get("congestion_level", "N/A")

            # Build popup content dynamically
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

        # Add circle marker for each site
        folium.CircleMarker(
            location=[lat, lon],
            radius=8,
            popup=popup_string,
            color=current_color,
            fill=True,
            fill_color=current_color,
            fill_opacity=0.6
        ).add_to(m)

       

    # Save the map to an HTML file
    # map_file = "map.html"
    m.save(map_file)

    

    # Encode to base64
    map_data = get_binary_file(map_file)
    b64_map = base64.b64encode(map_data).decode()

    # Create a download button
    with col1:
        st.download_button(
            label="📥 Download Map",
            data=map_data,
            file_name=map_file,
            mime="text/html"
        )


    # Render the map - Full width
    st_folium(m, width='100%', height=600, key="map_initial_load")


st.header("Pilot sites")
# st.write("Select a pilot site to view more")

# Table Headers
row_html_titles = f"""
    <div class="scalable-container">
        <div class="scrollable-row-titles">
            <div class="column">Pilot</div>
            <div class="column">Intervention Status</div>
            <div class="column">Score</div>
        </div>
    """


# Table Rows inside the same scrollable container
for site in pilots:
    # Determine intervention status
    intervention_start = site["intervention_start"]
    intervention_end = site["intervention_end"]
    start_date = datetime.strptime(intervention_start, "%Y-%m-%d")
    end_date = datetime.strptime(intervention_end, "%Y-%m-%d")
    current_time = datetime.strptime("2023-07-31", "%Y-%m-%d")  # IT IS STATIC TIME
    if start_date <= current_time <= end_date:
        interventions = "Ongoing"
    elif end_date < current_time:
        interventions = "Complete"
    else:
        interventions = "Planned"

    # Render the row inside a scrollable row
    row_html = f"""
    <div class="scrollable-row">
        <div class="column">
            <form action="/" method="get">
                <button class="city-button" type="submit" name="site" value="{site['name']}">{site['name']}</button>
            </form>
        </div>
        <div class="column">{interventions}</div>
        <div class="column">{random.randint(0, 100)}</div>
    </div>
    """
    row_html_titles += row_html
    # st.markdown(row_html, unsafe_allow_html=True)
row_html_titles += '</div>'
# Close the scrollable container
st.markdown(row_html_titles, unsafe_allow_html=True)

# Button click logic (simulated, replace with URL parameter handling)
# site_clicked = st.query_params.get("site")
# if site_clicked:
    # TODO: This action should open a new interface displaying KPI graphs
    # st.write(f"You clicked on {site_clicked}")

st.markdown(
    f"""
    <div class="footer-container">
        <div class="footer-text">
            © 2025 CERTH-ITI. All rights reserved.
        </div>
        <div class="footer-logos">
            <img src="data:image/jpeg;base64,{logo1_base64}" class="footer-logo" alt="ITI logo" />
            <img src="data:image/png;base64,{logo2_base64}" class="footer-logo" alt="REALLOCATE logo" />
        </div>
    </div>
    """,
    unsafe_allow_html=True
)





# Custom CSS styles
with open("./static/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


components.html(f"""
    <script>
        function sendMessage(sumi) {{
            const streamlitInput = window.parent.document.querySelector("input[pilots-testid='stTextInput']");
            streamlitInput.value = sumi;
            streamlitInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
    </script>
""", height=200)




# Render KPIs only if there is a selection
# if st.session_state.city:  # Check if there is a valid KPI selection
#     st.session_state.selected_kpi = selected_kpi
#     render_kpis(st.session_state.selected_kpi)  # Render only selected KPIs

# DONE
# Update indicator list based on finalized selection, include mapping to SUMI categories etc. (static indicator file)
# Create dummy data for the three current pilots for those indicators
# Make marker color change based on selected indicator
# Add tab explaining marker colors
# Fix marker coors to match the legend palette
# Add SUMI categories on display as clickable tabs, clicking them updates the map per SUMI category score
# Style city table at the bottom for flexibility
# Added selected KPI or SUMI on the title, adding it on the map legend proved to be buggy
# Pull weather and AQI data into json file from APIs
# Show weather and air quality from API in popup window on map
# The AirVisual API for air quality seems slightly unreliable, try another one. App works better with WAQI
# Button to export map if possible
# backend was created with the weather and AQI updates moved there.

# PRIORITIES
# TODO: Check if SUMI scores are calculated from KPIs (as average) and if not do it
# TODO: Log in and roles? (needs to be discussed though)
# TODO: Extra page per pilot site that shows: 1) Pilot description, 2) Pilot intervention dates 3) Milestone dates and status? (related to the T3.5 we took up)

# EXTRA
# TODO: On city selection, render different page (or stacked elements) for viewing every indicators plot after selecting it. Additional iformation about the indicator should also be displayed
# TODO: The titles in the city table at the bottom could become actionable buttons to rank cities based on column
# TODO: Style the SUMI buttons