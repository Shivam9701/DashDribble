import json
import sqlite3
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

# Get the absolute path of the SQLite database file and data folder
DB_FILE = os.getenv("DASHDRIBBLE_DB_FILE")
DATA_FOLDER = os.getenv("TEAM_DATA_FOLDER")


def create_tables(connection):
    """
    Create tables for league_teams, coaches, players, and stadiums.
    """
    cursor = connection.cursor()
    
    # Create the coaches table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coaches (
        id INTEGER PRIMARY KEY,
        team_id INTEGER,
        name TEXT,
        first_name TEXT,
        last_name TEXT,
        date_of_birth TEXT,
        nationality TEXT,
        contract_start TEXT,
        contract_until TEXT,
        FOREIGN KEY (team_id) REFERENCES league_teams (id)
    )
    """)

    # Create the players table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        team_id INTEGER,
        name TEXT,
        position TEXT,
        date_of_birth TEXT,
        nationality TEXT,
        FOREIGN KEY (team_id) REFERENCES league_teams (id)
    )
    """)

    # Create the stadiums table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stadiums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team_id INTEGER,
        venue_name TEXT,
        FOREIGN KEY (team_id) REFERENCES league_teams (id)
    )
    """)

    connection.commit()
    print(f"Created the coaches, players, and stadiums tables.")

def insert_coaches(connection, team_id, coach_data):
    """
    Insert data into the coaches table.
    """
    if not coach_data:
        return

    cursor = connection.cursor()
    
    # Check if the coach already exists
    cursor.execute("SELECT 1 FROM coaches WHERE id = ?", (coach_data["id"],))
    if cursor.fetchone():
        print(f"Coach with id {coach_data['id']} already exists. Skipping.")
        return
    
    cursor.execute("""
    INSERT INTO coaches (id, team_id, name, first_name, last_name, date_of_birth, nationality, contract_start, contract_until)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        coach_data["id"],
        team_id,
        coach_data["name"],
        coach_data.get("firstName", ""),
        coach_data.get("lastName", ""),
        coach_data.get("dateOfBirth", ""),
        coach_data.get("nationality", ""),
        coach_data.get("contract", {}).get("start", ""),
        coach_data.get("contract", {}).get("until", "")
    ))
    connection.commit()

def insert_players(connection, team_id, squad_data):
    """
    Insert data into the players table.
    """
    try:
        cursor = connection.cursor()
        for player in squad_data:
            
            # Check if the player already exists
            cursor.execute("SELECT 1 FROM players WHERE id = ?", (player["id"],))
            if cursor.fetchone():
                continue
            
            cursor.execute("""
            INSERT INTO players (id, team_id, name, position, date_of_birth, nationality)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                player["id"],
                team_id,
                player["name"],
                player.get("position", ""),
                player.get("dateOfBirth", ""),
                player.get("nationality", "")
            ))
        connection.commit()
    except sqlite3.Error as e:
        print(f"Error inserting player: {e}, player: {player}")

def insert_stadiums(connection, team_id, venue_name):
    """
    Insert data into the stadiums table.
    """
    cursor = connection.cursor()
    
    # Check if the stadium entry already exists
    cursor.execute("SELECT 1 FROM stadiums WHERE team_id = ? AND venue_name = ?", (team_id, venue_name))
    if cursor.fetchone():
        print(f"Stadium for team_id {team_id} already exists. Skipping.")
        return
    
    cursor.execute("""
    INSERT INTO stadiums (team_id, venue_name)
    VALUES (?, ?)
    """, (
        team_id,
        venue_name
    ))
    connection.commit()

def process_team_data(connection, data):
    """
    Iterate through the JSON data and populate all tables.
    """
    for team_id, team_data in data.items():
        team_id = int(team_id)
        
        # Insert into coaches table
        insert_coaches(connection, team_id, team_data.get("coach", {}))
        
        # Insert into players table
        insert_players(connection, team_id, team_data.get("squad", []))
        
        # Insert into stadiums table
        insert_stadiums(connection, team_id, team_data.get("venue", ""))
# Example Usage

if __name__ == "__main__":
    # Replace with the path to your JSON file
    json_file_path = f"{DATA_FOLDER}/team_data.json"

    try:
        with open(json_file_path, "r") as file:
            team_data = json.load(file)

        # Connect to SQLite database
        connection = sqlite3.connect(DB_FILE)
        
        if not connection:
            print("Error connecting to database.")

        # Create tables
        create_tables(connection)

        # Process data and populate tables
        process_team_data(connection, team_data)

        print("Data inserted successfully.")

    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
    except json.JSONDecodeError:
        print("Error decoding JSON.")
    finally:
        connection.close()
    