import sqlite3

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

def fetch_species_with_location():
    """Função para buscar dados de espécies com localização no banco de dados SQLite"""
    try:
        with sqlite3.connect('species.db') as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT name, latitude, longitude, image_path 
                FROM species 
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            """)
            records = cursor.fetchall()

        return records

    except sqlite3.Error as e:
        st.error(f"Error connecting to SQLite database: {e}")
        return []

# Function to initialize the database and create the species table
def init_db():
    try:
        # Establish a database connection (SQLite)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS species (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date DATE NOT NULL,
                longitude TEXT,
                latitude TEXT,
                image_path TEXT
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database and table initialized.")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")

# Function to add a species to the database
def add_species(name, date, lon, lat, image_path):
    try:
        # Establish a database connection (SQLite)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Insert data into species table
        cursor.execute("""
            INSERT INTO species (name, date, longitude, latitude, image_path)
            VALUES (?, ?, ?, ?, ?);
        """, (name, date, lon, lat, image_path))

        # Commit the transaction
        conn.commit()

        cursor.close()
        conn.close()
        print("Species added to database.")
    except sqlite3.Error as e:
        print(f"Error adding species to database: {e}")