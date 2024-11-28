import streamlit as st
import sqlite3
from streamlit_folium import st_folium
import folium

# Function to fetch species with location from SQLite database
def fetch_species_with_location():
    try:
        # Establish connection to SQLite DB
        conn = sqlite3.connect('species.db')  # Ensure you use the correct path for the SQLite DB
        cursor = conn.cursor()

        # SQL query to fetch species with non-null latitude and longitude
        cursor.execute("""
            SELECT name, latitude, longitude, image_path 
            FROM species 
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
        """)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records
    except sqlite3.Error as e:
        st.error(f"Error connecting to SQLite database: {e}")
        return []

# Function to display the map with species markers
def display_map():
    species_data = fetch_species_with_location()

    if not species_data:
        st.write("No species data available with location.")
        return

    # Initialize the map with the first species' coordinates
    map_center = [float(species_data[0][1]), float(species_data[0][2])] if species_data else [0, 0]
    map_obj = folium.Map(location=map_center, zoom_start=5)

    # Add markers for each species
    for species in species_data:
        name, lat, lon, _ = species
        popup_content = f"<b>{name}</b>"
        folium.Marker([float(lat), float(lon)], popup=popup_content).add_to(map_obj)

    # Display the map in Streamlit
    st_folium(map_obj, width=725)

# Call the function to display the map with species
display_map()
