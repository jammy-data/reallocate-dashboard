import os
import io
import requests
import pandas as pd
from ckanapi import RemoteCKAN
import streamlit as st

@st.cache_data(show_spinner="Loading dataset...")
def load_parquet_from_ckan(dataset_name: str, ckan_url: str = "https://reallocate-ckan.iti.gr") -> pd.DataFrame:
    """
    Fetches the URL of a Parquet resource from the specified CKAN dataset
    and returns it as a Pandas DataFrame.

    Args:
        dataset_name (str): The name of the dataset in CKAN.
        ckan_url (str, optional): The base URL of the CKAN instance. Defaults to Reallocate's CKAN.

    Returns:
        pd.DataFrame: The DataFrame loaded from the Parquet resource.

    Raises:
        ValueError: If no Parquet URL is found or if the download fails.
    """
    api_key = os.getenv("REALLOCATE_KEY")
    if not api_key:
        raise EnvironmentError("Environment variable REALLOCATE_KEY is not set.")

    ckan = RemoteCKAN(ckan_url, apikey=api_key)

    try:
        dataset = ckan.action.package_show(id=dataset_name)
    except Exception as e:
        raise ValueError(f"Failed to fetch dataset metadata for '{dataset_name}': {e}")

    parquet_url = None
    for res in dataset.get("resources", []):
        if res.get("format", "").lower() == "parquet":
            parquet_url = res.get("url")
            break

    if not parquet_url:
        raise ValueError(f"No Parquet resource found in dataset '{dataset_name}'.")

    response = requests.get(parquet_url, headers={"Authorization": api_key})
    if response.status_code != 200:
        raise ValueError(f"Failed to download Parquet file. HTTP status code: {response.status_code}")

    df = pd.read_parquet(io.BytesIO(response.content))
    return df
