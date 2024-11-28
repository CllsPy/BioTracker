import streamlit as st
import sqlite3
from streamlit_folium import st_folium
import folium

# Function to fetch species with location from SQLite database
def fetch_species_with_location():
    try:
        # Establish connection to SQLite DB using a context manager for auto-close
        with sqlite3.connect('species.db') as conn:
            cursor = conn.cursor()

            # SQL query to fetch species with non-null latitude and longitude
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

# Function to display the map with species markers
def display_map():
    species_data = fetch_species_with_location()

    if not species_data:
        st.write("No species data available with location.")
        return

    # Initialize the map with the first species' coordinates
    first_species = species_data[0]
    map_center = [float(first_species[1]), float(first_species[2])] if first_species else [0, 0]
    
    # Create the folium map
    map_obj = folium.Map(location=map_center, zoom_start=12)

    # Add markers for each species
    for species in species_data:
        name, lat, lon, _ = species
        try:
            lat = float(lat)
            lon = float(lon)
            
            # Validate coordinates: latitude between -90 and 90, longitude between -180 and 180
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                #popup_content = f"<b>{name}</b>"
                folium.Marker([lat, lon]).add_to(map_obj)
            else:
                st.warning(f"Invalid coordinates for species: {name} (Lat: {lat}, Lon: {lon})")
        except ValueError:
            st.warning(f"Invalid latitude or longitude for species: {name} (Lat: {lat}, Lon: {lon})")

    # Display the map in Streamlit
    st_folium(map_obj)

# Call the function to display the map with species
display_map()
