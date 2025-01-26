import requests
import json
import dotenv
import os
import time

dotenv.load_dotenv()

API_URL = os.getenv("FOOTBALL_DATA_ORG_URL")
API_TOKEN = os.getenv("FOOTBALL_DATA_ORG_TOKEN")

competitions = [
    "PL",
    "PD",
    "SA",
    "BL1",
    "FL1",
]

def get_team_ids():
    all_teams = {}
    
    for competition in competitions:
        try:
            with open(f"data/current_league_teams/{competition}.json", "r") as f:
                data = json.load(f)
            
            team_ids = [item["team"]["id"] for item in data["standings"][0]["table"]]
            all_teams[competition] = team_ids
        
        except FileNotFoundError:
            print(f"File not found: {competition}.json")
            continue
        except json.JSONDecodeError:
            print(f"Error decoding {competition}.json")
            continue
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    return all_teams
    
def get_players_by_team_id(team_id):
    url = f"{API_URL}/teams/{team_id}"
    headers = {
        "X-Auth-Token": API_TOKEN
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch players for team {team_id}: {response.status_code}")
            return None
        
    except requests.RequestException as e:
        print(f"Request error for team {team_id}: {e}")
        return None

def fetch_all_players(team_ids):
    """
    Fetches player data for all teams with a request rate limit of 9 requests/minute.

    Args:
        team_ids (list): List of team IDs.

    Returns:
        dict: Dictionary of team IDs and their player data.
    """
    player_data = {}
    requests_per_minute = 9
    delay_between_requests = 60 / requests_per_minute

    for i, team_id in enumerate(team_ids):
        print(f"Fetching players for team {team_id} ({i+1}/{len(team_ids)})...")
        data = get_players_by_team_id(team_id)
        if data:
            player_data[team_id] = data
        
        # Enforce rate limiting
        if (i + 1) % requests_per_minute == 0:
            print("Rate limit reached. Waiting for 1 minute...")
            time.sleep(60)
        else:
            time.sleep(delay_between_requests)

    return player_data

all_teams = get_team_ids()

all_team_ids = []

for competition in all_teams:
    all_team_ids.extend(all_teams[competition])
    
player_data = fetch_all_players(all_team_ids)

with open("data/team_data/team_data.json", "w") as f:
    json.dump(player_data, f, indent=4)
