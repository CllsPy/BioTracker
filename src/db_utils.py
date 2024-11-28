import sqlite3
import os

# SQLite database path (relative path for SQLite file)
DB_PATH = 'species.db'  # Path to your SQLite database file

# Function to create a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

# Create or connect to the database and initialize the table
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create table if not exists (SQLite syntax)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS species (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species_name TEXT NOT NULL,
        date_observed DATE NOT NULL,
        latitude TEXT,
        longitude TEXT,
        photo_path TEXT
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Function to add a record
def add_species(species_name, date_observed, latitude, longitude, photo_path):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO species (species_name, date_observed, latitude, longitude, photo_path)
    VALUES (?, ?, ?, ?, ?)
    """, (species_name, date_observed, latitude, longitude, photo_path))

    conn.commit()
    cursor.close()
    conn.close()

# Fetch all records
def fetch_species():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM species")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

# Function to clear the database (delete all records)
def clear_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete all rows in the species table (SQLite syntax)
    cursor.execute("DELETE FROM species")
    
    # SQLite does not support TRUNCATE TABLE like MySQL, so we use DELETE
    # If you want to reset the auto-increment value, you can execute this:
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='species'")
    
    conn.commit()
    cursor.close()
    conn.close()
