import sqlite3
import json
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

# Get the absolute path of the SQLite database file and data folder
DB_FILE = os.getenv("DASHDRIBBLE_DB_FILE")
DATA_FOLDER = os.getenv("LEAGUE_TEAMS_DATA_FOLDER")


# Create the schema for the league_teams table
def create_league_teams_schema(cursor):
    try:
        # Create the static table: teams
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS league_teams (
            id INTEGER PRIMARY KEY,
            league_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            short_name TEXT,
            tla TEXT,
            crest TEXT,
            FOREIGN KEY (league_id) REFERENCES leagues (id)
        );
        """)

        # Create the dynamic table: league_teams
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS current_standings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            league_id INTEGER NOT NULL,
            team_id INTEGER NOT NULL,
            position INTEGER,
            played_games INTEGER,
            won INTEGER,
            draw INTEGER,
            lost INTEGER,
            points INTEGER,
            goals_for INTEGER,
            goals_against INTEGER,
            goal_difference INTEGER,
            FOREIGN KEY (league_id) REFERENCES leagues (id),
            FOREIGN KEY (team_id) REFERENCES league_teams (id)
        );
        """)

        # Commit the changes and close the connection
        cursor.connection.commit()
        print(
            "Tables 'league_teams' and 'current_standings' created successfully/already exists."
        )

    except sqlite3.Error as e:
        print(f"An error occurred while creating tables: {e}")


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


# Step 1: Parse JSON Data
def parse_json_data(json_data):
    """Parse JSON data to extract league and team details."""
    league_id = json_data["competition"]["id"]

    static_teams = []  # For static table: league_teams
    dynamic_standings = []  # For dynamic table: current_standings

    for standing in json_data["standings"]:
        for entry in standing["table"]:
            # Static data for league_teams
            static_team_data = {
                "league_id": league_id,
                "id": entry["team"]["id"],
                "name": entry["team"]["name"],
                "short_name": entry["team"].get("shortName", ""),
                "tla": entry["team"].get("tla", ""),
                "crest": entry["team"].get("crest", ""),
            }
            static_teams.append(static_team_data)

            # Dynamic data for current_standings
            dynamic_data = {
                "league_id": league_id,
                "team_id": entry["team"]["id"],
                "position": entry["position"],
                "played_games": entry["playedGames"],
                "won": entry["won"],
                "draw": entry["draw"],
                "lost": entry["lost"],
                "points": entry["points"],
                "goals_for": entry["goalsFor"],
                "goals_against": entry["goalsAgainst"],
                "goal_difference": entry["goalDifference"],
            }
            dynamic_standings.append(dynamic_data)

    return static_teams, dynamic_standings


# Step 2: Insert Team Data for league_teams (static table)
def insert_team(cursor, table_name, data):
    """Insert a single record into the given table."""
    try:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data.keys()])
        sql = f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(data.values()))

    except sqlite3.Error as e:
        print(f"Database Error inserting team: {e}")
    except Exception as e:
        print(f"Error inserting into {table_name}: {e}")


# Step 3: Insert All Teams into league_teams and current_standings
def insert_teams(cursor, data_folder):
    """Insert team data into static (league_teams) and dynamic (current_standings) tables."""
    try:
        for filename in os.listdir(data_folder):
            if filename.endswith(".json"):
                # Step 1: Load and parse JSON data
                json_data = get_json_data(f"{data_folder}/{filename}")
                static_teams, dynamic_standings = parse_json_data(json_data)

                # Step 2: Insert into league_teams (static data)
                for team in static_teams:
                    insert_team(cursor, "league_teams", team)

                # Step 3: Insert into current_standings (dynamic data)
                for standing in dynamic_standings:
                    insert_team(cursor, "current_standings", standing)

                print(f"Inserted teams and standings for {filename}")

        # Commit changes after processing all files
        cursor.connection.commit()
        print("Teams and standings inserted successfully.")

    except sqlite3.Error as e:
        print(f"Database Error inserting teams and standings: {e}")

    except Exception as e:
        print(f"Error inserting teams and standings: {e}")


def main():
    # Connect to SQLite database (or create a new one)
    try:
        print(f"Connecting to database... {DB_FILE}")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        print("Database connected successfully.")

        # Create the schema for the league_teams table
        create_league_teams_schema(cursor)

        # Insert team data into league_teams and current_standings tables
        insert_teams(cursor, DATA_FOLDER)

        # Close the database connection
        conn.close()

    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")


if __name__ == "__main__":
    main()
