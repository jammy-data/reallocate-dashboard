"""Streamlit app to fetch and display datasets from a given API with caching and error handling."""
import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point
from dotenv import load_dotenv

# Ensure the project root is in sys.path for module discovery
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# -----------------------------------------------------------------

from ckanapi import RemoteCKAN
from helper_functions import load_parquet_from_ckan

load_dotenv()
#st.logo("images/reallocate_logo.png", size = 'large')


DATASETS = {
    "Walking journeys": "trips_walking",
    "Bike & PMV by sex": "bike_and_pmv_by_sex",
    "Public accessibility": "streets_accessibility"
}
#Add a home button to go back to the homepage
if st.button("Homepage"):
    st.switch_page("pages/Home.py")

# Streamlit dropdown
st.title("Dataset Explorer")
dataset_name = st.selectbox("Choose a dataset", list(DATASETS.keys()))

# Fetch data
url = DATASETS[dataset_name]

df = load_parquet_from_ckan(url)


try:
    st.write(f"Preview of **{dataset_name}**:")
    st.dataframe(df.head())
    # Exclude 'Dim-00:TEMPS' from VARIABLES
#    # We need to create a specific if function to handle geographic dataframes
    if 'Gis_X' in df.columns:
        # Create a GeoDataFrame from the DataFrame
        geometry = [Point(xy) for xy in zip(df['Gis_X'], df['Gis_Y'])]
        gdf = gpd.GeoDataFrame(df, geometry = geometry, crs="EPSG:25831")
        gdf = gdf.to_crs(epsg=4326)
        gdf["lati"] = gdf.geometry.y
        gdf["longi"] = gdf.geometry.x
        fig = px.scatter_map(
            gdf,
            lat=gdf['lati'],
            lon=gdf["longi"],
            color='Situació',
            zoom = 10,
            hover_data = {"Data d'Alta":True,
                       "Situació": True,
                       "lati": False,
                       "longi": False},
       )
        fig.update_layout(map_style="carto-darkmatter")
        st.plotly_chart(fig)
    else:
        VARIABLES = [col for col in df.columns if col != 'Dim-00:TEMPS']
        variable_name = st.selectbox("Choose a variable", VARIABLES)
        grouped = df.groupby(['Dim-00:TEMPS', variable_name]).sum()
        grouped['VALUE'].unstack(variable_name)
        grouped = grouped.reset_index()
    # Two columns
 #   col1, col2 = st.columns(2)
 #   with col1:
    # Simple Plotly graph
        fig = px.line(grouped, x=grouped['Dim-00:TEMPS'], y=grouped['VALUE'], color= variable_name,title=f"{dataset_name} Overview")
        st.plotly_chart(fig)

except Exception as e:
    st.error(f"Failed to load data: {e}")

##########################################################
st.write("---")

# --- Define paths and links for both images ---
# Image 1
image_path_1 = "https://reallocatemobility.eu/maintemplate/data/logos/logo.png"
link_url_1 = "https://reallocatemobility.eu"
alt_text_1 = "Reallocate Logo - Click to go to Google"

# Image 2
image_path_2 = "https://www.bsc.es/sites/default/files/public/styles/bscw2_-_simple_crop_style/public/bscw2/pages/discover-bsc/bsc-branding-identity-logo-header_0.jpg?itok=BdjkMwL6&sc=569a3a63c536723072a6d292da3890ca"
link_url_2 = "https://www.bsc.es" # Replace with your second link
alt_text_2 = "Partner Logo - Click to go to Example.com"

# --- Inject Custom CSS for Flexbox Layout ---
st.markdown(
    """
    <style>
    .image-container {
        display: flex; /* Makes the images display in a row */
        justify-content: center; /* Centers the images horizontally */
        align-items: center; /* Vertically aligns images if they have different heights */
        gap: 20px; /* Adds space between the images */
        margin-top: 20px; /* Add some space above the container */
        margin-bottom: 20px; /* Add some space below the container */
    }

    .image-container img {
        height: auto; /* Maintain aspect ratio */
        max-height: 80px; /* Set a max height for both images */
        width: auto; /* Let width adjust based on height */
        max-width: 150px; /* Set a max width for both images */
        /* Add any other common styling here, e.g., border, border-radius */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Use Markdown to embed HTML with both linked images ---
st.markdown(
    f"""
    <div class="image-container">
        <a href="{link_url_1}" target="_blank">
            <img src="{image_path_1}" alt="{alt_text_1}">
        </a>
        <a href="{link_url_2}" target="_blank">
            <img src="{image_path_2}" alt="{alt_text_2}">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("---")