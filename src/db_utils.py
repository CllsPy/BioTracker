import psycopg2
import os

# PostgreSQL connection parameters
DB_HOST = "localhost"  # Replace with your PostgreSQL host, e.g., "localhost" or a cloud DB URL
DB_PORT = "5432"       # Default PostgreSQL port
DB_NAME = "species_db" # Your database name
DB_USER = "your_user"   # Your PostgreSQL username
DB_PASSWORD = "your_password" # Your PostgreSQL password

# Function to create a connection to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

# Create or connect to the database and initialize the table
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS species (
        id SERIAL PRIMARY KEY,
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
    VALUES (%s, %s, %s, %s, %s)
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

    # Delete all rows in the species table
    cursor.execute("DELETE FROM species")
    
    # Reset the auto-increment ID (optional)
    cursor.execute("TRUNCATE TABLE species RESTART IDENTITY")
    
    conn.commit()
    cursor.close()
    conn.close()
