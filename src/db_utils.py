import sqlite3
from data import *

# Create or connect to the database
def init_db():
    conn = sqlite3.connect("data/species.db")
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS species (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        species_name TEXT,
        date_observed DATE,
        latitude TEXT,
        longitude TEXT,
        photo_path TEXT
    )
    """)
    conn.commit()
    conn.close()

# Function to add a record
def add_species(species_name, date_observed, longitude, latitude, photo_path):
    conn = sqlite3.connect("data/species.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO species (species_name, date_observed, latitude, longitude, photo_path)
    VALUES (?, ?, ?, ?, ?)
    """, (species_name, date_observed, latitude, longitude, photo_path))
    
    conn.commit()
    conn.close()

# Fetch all records
def fetch_species():
    conn = sqlite3.connect("data/species.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM species")
    records = cursor.fetchall()
    conn.close()
    return records


def clear_database():
    conn = sqlite3.connect("data/species.db")
    cursor = conn.cursor()

    # Delete all rows in the species table
    cursor.execute("DELETE FROM species")
    
    # Reset the auto-increment ID (optional)
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='species'")
    
    conn.commit()
    conn.close()
