import streamlit as st
from db_utils import fetch_species
import folium
from streamlit_folium import st_folium
import psycopg2

# Function to fetch species with location from PostgreSQL database
def fetch_species_with_location():
    conn = psycopg2.connect(
        host="localhost",  # Replace with your PostgreSQL host
        port="5432",       # Default PostgreSQL port
        dbname="species_db",  # Your database name
        user="your_user",  # Your PostgreSQL username
        password="your_password"  # Your PostgreSQL password
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT species_name, latitude, longitude, photo_path 
        FROM species 
        WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    """)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

# Function to display the map with species markers
def display_map():
    species_data = fetch_species_with_location()

    # Initialize a map
    map_center = [0, 0] if not species_data else [species_data[0][1], species_data[0][2]]
    map_obj = folium.Map(location=map_center, zoom_start=5)

    # Add markers for each species
    for species in species_data:
        name, lat, lon, _ = species
        popup_content = f"<b>{name}</b>"
        folium.Marker([lat, lon], popup=popup_content).add_to(map_obj)

    # Display the map in Streamlit
    st_folium(map_obj, width=725)

# Call the function in your Streamlit app
display_map()
