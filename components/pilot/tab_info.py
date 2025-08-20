import streamlit as st
import pandas as pd
import pydeck as pdk
from shapely.geometry import shape
from utils.maps import get_view_state_from_geometry
def render(info):
    st.markdown("### Description")
    st.write(info.get("description", "No description available."))

    st.markdown(f"### Location, {info.get('location', 'No location provided.')}")

    if "geometry" not in info or not info["geometry"]:
        st.write("Map data not available.")
        return

    try:
        geom = shape(info["geometry"])  # Convert GeoJSON to shapely geometry

        layers = []
        initial_view = {
            "latitude": geom.centroid.y,
            "longitude": geom.centroid.x,
            "zoom": 13,
            "pitch": 0,
        }

        if geom.geom_type in ["Polygon", "MultiPolygon"]:
            layers.append(
                pdk.Layer(
                    "GeoJsonLayer",
                    data={
                        "type": "Feature",
                        "geometry": info["geometry"],
                        "properties": {},
                    },
                    stroked=True,
                    filled=True,
                    get_fill_color=[0, 100, 200, 80],
                    get_line_color=[0, 0, 0],
                    line_width_min_pixels=1,
                )
            )
            view_state = get_view_state_from_geometry(geom)

            st.pydeck_chart(pdk.Deck(
                initial_view_state=view_state,
                layers=layers,
                map_style="mapbox://styles/mapbox/light-v9"  # 👈 Light background
            ))

        elif geom.geom_type == "Point":
            view_state = pdk.ViewState(
                latitude=geom.y,
                longitude=geom.x,
                zoom=12,  # Try 11–12 for city-level view
                pitch=0
            )

            st.pydeck_chart(pdk.Deck(
                initial_view_state=view_state,
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=pd.DataFrame({
                            "lat": [geom.y],
                            "lon": [geom.x]
                        }),
                        get_position='[lon, lat]',
                        get_fill_color='[0, 100, 200, 160]',
                        get_radius=100,
                    )
                ],
                map_style="mapbox://styles/mapbox/light-v9"
            ))


        else:
            st.warning(f"Unsupported geometry type: {geom.geom_type}")
            return

    except Exception as e:
        st.error(f"Failed to render geometry: {e}")
    