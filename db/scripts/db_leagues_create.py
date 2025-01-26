import sqlite3
import json
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

# Get the absolute path of the SQLite database file and data folder
DB_FILE = os.getenv("DASHDRIBBLE_DB_FILE")
DATA_FOLDER = os.getenv("LEAGUE_DATA_FOLDER")


# Utility function to get JSON data (for example)
def get_json_data(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def parse_json_data(data: dict):
    try:
        # Assuming the structure is consistent and needs parsing
        league = {
            "id": data["id"],
            "name": data["name"],
            "code": data["code"],
            "emblem": data["emblem"],
            "current_season_id": data["currentSeason"]["id"],
            "current_matchday": data["currentSeason"]["currentMatchday"],
            "area_id": data["area"]["id"],
            "area_name": data["area"]["name"],
            "area_code": data["area"]["code"],
            "area_flag": data["area"]["flag"],
        }
        return league
    except KeyError as e:
        print(f"Missing expected key in JSON data: {e}")
        return None
    except Exception as e:
        print(f"Error parsing JSON data: {e}")
        return None


def insert_league(cursor, league):
    try:
        cursor.execute(
            """
            INSERT INTO leagues (
                id, name, code, emblem, current_season_id,
                area_id, area_name, area_code, area_flag
            ) VALUES (
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?
            )
            """,
            (
                league["id"],
                league["name"],
                league["code"],
                league["emblem"],
                league["current_season_id"],
                league["area_id"],
                league["area_name"],
                league["area_code"],
                league["area_flag"],
            ),
        )
    except sqlite3.Error as e:
        print(f"Database Error inserting league: {e}")
    except Exception as e:
        print(f"Unexpected Error inserting league: {e}")


def insert_leagues(cursor, data_folder):
    try:
        for filename in os.listdir(data_folder):
            if filename.endswith(".json"):
                data = get_json_data(f"{data_folder}/{filename}")

                # Parse the JSON data
                league = parse_json_data(data)

                # Insert the league into the database
                insert_league(cursor, league)

                print(f"Inserted league: {league['name']}")

        # Commit the changes
        cursor.connection.commit()
        print("Leagues inserted successfully.")

    except sqlite3.Error as e:
        print(f"Database Error inserting leagues: {e}")
    except Exception as e:
        print(f"Error inserting leagues: {e}")


def main():
    # Connect to SQLite database (or create a new one)
    try:
        print(f"Connecting to database... {DB_FILE}")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        print("Database connected successfully.")

        # Create the leagues table
        insert_leagues(cursor, DATA_FOLDER)

        # Check the leagues table
        cursor.execute("SELECT * FROM leagues")
        leagues = cursor.fetchall()
        print(leagues)

        # Close the database connection
        conn.close()

    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")


if __name__ == "__main__":
    main()
