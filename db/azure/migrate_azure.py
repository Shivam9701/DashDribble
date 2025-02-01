import sqlite3
import os
import pandas as pd
from sqlalchemy import create_engine
import dotenv
import urllib.parse

# Load environment variables
dotenv.load_dotenv()

# SQLite DB file path
sqlite_db_path = os.environ.get("DASHDRIBBLE_DB_FILE")

# Create a connection string for Azure SQL
azure_connection_string = os.environ.get("AZURE_CONN_STRING")
params = urllib.parse.quote(azure_connection_string)

url = f"mssql+pyodbc:///?odbc_connect={params}"


try:
    # Connect to SQLite
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_cursor = sqlite_conn.cursor()
    
    # Connect to Azure SQL using SQLAlchemy
    azure_engine = create_engine(url)
except sqlite3.Error as e:
    print(f"SQLite error: {e}")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Fetch all table names from SQLite
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in sqlite_cursor.fetchall()]

# Loop through each table and migrate
for table in tables:
    print(f"Migrating table: {table}")

    # Read table data from SQLite
    df = pd.read_sql(f"SELECT * FROM {table}", sqlite_conn)

    # Upload data to Azure SQL
    df.to_sql(table, azure_engine, if_exists="replace", index=False)
    print(f"Successfully migrated: {table}")

# Close connections
sqlite_conn.close()
print("Migration completed successfully!")
