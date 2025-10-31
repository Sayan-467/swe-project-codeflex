import json
import os
from datetime import datetime

DATA_PATH = os.path.join("data", "user_progress.json")

def load_data():
    if not os.path.exists(DATA_PATH):
        return {}
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    os.makedirs("data", exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

def update_progress(platform, handle, score):
    data = load_data()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if platform not in data:
        data[platform] = {}

    if handle not in data[platform]:
        data[platform][handle] = []

    data[platform][handle].append({
        "timestamp": timestamp,
        "score": score
    })

    save_data(data)
    return data[platform][handle]

def get_progress_history(platform, handle):
    data = load_data()
    if platform in data and handle in data[platform]:
        return data[platform][handle]
    return []
