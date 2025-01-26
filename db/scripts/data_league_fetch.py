import requests
import json
import dotenv
import os

dotenv.load_dotenv()

API_URL = os.getenv("FOOTBALL_DATA_ORG_URL")
API_TOKEN = os.getenv("FOOTBALL_DATA_ORG_TOKEN")

competitions = [  # "PL",
    "PD",
    "SA",
    "BL1",
    "FL1",
]

for competition in competitions:
    response = requests.get(
        f"{API_URL}/competition/{competition}", headers={"X-Auth-Token": API_TOKEN}
    )
    data = response.json()
    with open(f"data/historical_winners/{competition}.json", "w") as f:
        json.dump(data, f)
