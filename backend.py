import json
import time
import schedule
import threading  # To run scheduling in a separate thread
from fastapi import FastAPI, APIRouter, HTTPException
import uvicorn
import sys
import os
sys.path.append(os.path.abspath("utils"))  # adjust relative path
from helper_functions import update_weather, update_aqi, update_traffic
import pandas as pd
# from motor.motor_asyncio import AsyncIOMotorClient
from typing import Dict
from pydantic import BaseModel
from datetime import datetime

class KPIPost(BaseModel):
    pilot_id: str
    timestamp: datetime
    kpis: Dict[str, float]  # Flexible keys, but all values expected as floats


# client = AsyncIOMotorClient("mongodb://localhost:27017")
# db = client["kpi_database"]  # or whatever name you prefer
# kpi_collection = db.get_collection("kpis")


app = FastAPI()

pilots_static_df = pd.read_excel('./config/pilot_static_data.xlsx', engine="openpyxl")
locations = {row['name']: {"lat": row['lat'], "lon": row['lon']} for index, row in pilots_static_df.iterrows()}
# Load pilot site locations
# with open("./pilot_sites.json") as f:
#     pilots = json.load(f)

# locations = {pilot['name']: {"lat": pilot['coordinates'][0], "lon": pilot['coordinates'][1]} for pilot in pilots}

# async def add_kpi(pilot_id: str, kpis: dict, timestamp: datetime):
#     timestamp_key = timestamp.isoformat()  # Convert to string for Mongo key

#     result = await kpi_collection.update_one(
#         {"pilot_id": pilot_id},
#         {"$set": {f"kpis.{timestamp_key}": kpis}},
#         upsert=True
#     )

#     return f"Updated pilot {pilot_id} with timestamp {timestamp_key}"

# async def get_kpis(pilot_id: str):
#     kpis = await kpi_collection.find({"pilot_id": pilot_id}).to_list(100)
#     # Convert ObjectId to string
#     for kpi in kpis:
#         kpi["_id"] = str(kpi["_id"])
#     return kpis


router = APIRouter()

# async def create_kpi(pilot_id: str, payload: KPIPost):
#     if str(pilot_id) not in locations.keys():
#         raise HTTPException(status_code=404, detail="Pilot ID not found")
#     if pilot_id != payload.pilot_id:
#         raise HTTPException(status_code=400, detail="Mismatch in pilot_id")
    
#     await kpi_collection.update_one(
#         {"pilot_id": pilot_id},
#         {"$set": {f'kpis.{payload.timestamp}': payload.kpis}},
#         upsert=True # will handle duplicate entries
#     )
#     return {"status": "success"}


# @router.get("/get_kpi_values/")
# async def read_kpis(pilot_id: str):
#     data = await get_kpis(pilot_id)
#     if not data:
#         raise HTTPException(status_code=404, detail="KPIs not found")
#     return data


# Initial data update
update_weather(locations)
update_aqi(locations)
update_traffic(locations)

# endpoint to access the pilot site json data
@router.get("/pilot_api_data")
def get_weather(site_name: str):
    try:
        """Fetch weather data for the requested location."""
        with open("./data/pilot_weather.json") as f2:
            pilot_weather = json.load(f2)
            return {"site": site_name, site_name: pilot_weather['locations'].get(site_name, "No data")}
    except json.JSONDecodeError:
        print("Failed to load API data")
        return {"error": "Failed to load weather data"}

app.include_router(router)

def schedule_updates():
    """Schedule background updates for weather, AQI, and traffic data."""
    schedule.every(60).minutes.do(update_weather, locations=locations)  # Weather update (hourly)
    schedule.every(60).minutes.do(update_aqi, locations=locations)      # AQI update (hourly)
    schedule.every(15).minutes.do(update_traffic, locations=locations)  # Traffic update (every 15 mins)

    while True:
        schedule.run_pending()
        time.sleep(300)  # Wait 5 minutes before checking again

# Start the scheduler in a separate thread
def start_scheduler():
    scheduler_thread = threading.Thread(target=schedule_updates, daemon=True)
    scheduler_thread.start()

if __name__ == "__main__":
    start_scheduler()  # Start scheduling in the background
    uvicorn.run(app, host="0.0.0.0", port=8000)