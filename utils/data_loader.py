import os
import json

def load_generic_data(data_dir="config/"):
    pilots = []
    with open(os.path.join(data_dir, "pilots.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, list):
            pilots.extend(data)
        else:
            pilots.append(data)
    return pilots

def load_all_pilots(data_dir="config/pilots"):
    pilots = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            with open(os.path.join(data_dir, filename), "r", encoding="utf-8") as f:
                pilot_data = json.load(f)
                pilots.append(pilot_data)
    return pilots

def load_kpi(data_dir="config/"):
    with open(os.path.join(data_dir, "kpi.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
        return data if isinstance(data, list) else [data]

def load_pilot_data(pilot_id):
    path = os.path.join("data", "pilots", f"{pilot_id}.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def load_logos(dir="./config/"):
    with open(os.path.join(dir, "logos.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    if data is None:
        return ["Hello"]
    return data