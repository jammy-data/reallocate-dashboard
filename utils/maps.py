from pydeck.data_utils.viewport_helpers import compute_view
import pydeck as pdk
import pandas as pd

def get_view_state_from_geometry(geom):
    # Get the bounds of the geometry
    bounds = geom.bounds  # (minx, miny, maxx, maxy)
    min_lon, min_lat, max_lon, max_lat = bounds

    # Convert to DataFrame of points (corners of the bounds)
    df = pd.DataFrame({
        "lon": [min_lon, max_lon],
        "lat": [min_lat, max_lat]
    })

    # pydeck expects lat/lon columns
    return compute_view(df)
