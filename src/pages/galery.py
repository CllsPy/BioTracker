import streamlit as st
import sqlite3
from streamlit_folium import st_folium
import folium

def fetch_species_with_location():
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

def display_map():
    species_data = fetch_species_with_location()

    if not species_data:
        st.write("No species data available with location.")
        return

    first_species = species_data[0]
    map_center = [float(first_species[1]), float(first_species[2])] if first_species else [0, 0]
    map_obj = folium.Map(location=map_center, zoom_start=5)

    for species in species_data:
        name, lat, lon, _ = species
        try:
            lat = float(lat)
            lon = float(lon)
            
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                popup_content = f"<b>{name}</b>"
                folium.Marker([lat, lon], popup=popup_content).add_to(map_obj)
            else:
                st.warning(f"Invalid coordinates for species: {name} (Lat: {lat}, Lon: {lon})")
        except ValueError:
            st.warning(f"Invalid latitude or longitude for species: {name} (Lat: {lat}, Lon: {lon})")

    # Display the map in Streamlit
    st_folium(map_obj, width=725)

    # Force a rerun to ensure the map is rendered properly
    st.experimental_rerun()

# Call the function to display the map with species
display_map()
