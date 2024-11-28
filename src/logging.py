import sqlite3
import datetime
import streamlit as st
import os

# SQLite database configuration
DB_PATH = 'species.db'  # SQLite uses a file-based DB

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

# Streamlit app
init_db()  # Ensures the database and table are created

with st.form("Cadastro do Animal"):
    st.write("Upload")
    uploaded_img = st.file_uploader('Image')

    name = st.text_input('Nome do Animal')
    date = st.date_input("Date", datetime.date(2019, 7, 6))
    lon = st.text_input('longitude')
    lat = st.text_input('latitude')

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.image(uploaded_img)

        # Save the image to a file path (make sure directory exists)
        if not os.path.exists("uploaded_images"):
            os.makedirs("uploaded_images")
        
        image_path = f"uploaded_images/{uploaded_img.name}"  # Example directory for saving images
        with open(image_path, "wb") as img_file:
            img_file.write(uploaded_img.getbuffer())

        # Add the species info to the SQLite database
        add_species(name, date, lon, lat, image_path)
