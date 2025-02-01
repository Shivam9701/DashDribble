import sqlite3
import json

# Connect to SQLite database
sqlite_db_path = "dashdribble.db"
sqlite_conn = sqlite3.connect(sqlite_db_path)
sqlite_cursor = sqlite_conn.cursor()

# Get all tables
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in sqlite_cursor.fetchall()]

# Store foreign key constraints
foreign_keys = []

for table in tables:
    sqlite_cursor.execute(f"PRAGMA foreign_key_list({table});")
    fks = sqlite_cursor.fetchall()
    
    for fk in fks:
        foreign_keys.append({
            "table": table,
            "column": fk[3],  # Column in the current table
            "ref_table": fk[2],  # Referenced table
            "ref_column": fk[4],  # Referenced column
        })


print("Foreign keys extracted ", foreign_keys)
# Save foreign keys to a JSON file
with open("foreign_keys.json", "w") as f:
    json.dump(foreign_keys, f, indent=4)

sqlite_conn.close()
print("Foreign keys extracted and saved to foreign_keys.json")
