import streamlit as st
import sqlite3
from streamlit_leaflet import st_leaflet

# Função para buscar dados de espécies com localização no banco de dados SQLite
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

# Função para exibir o mapa com marcadores de espécies
def display_map():
    species_data = fetch_species_with_location()

    if not species_data:
        st.write("No species data available with location.")
        return

    # Preparando os marcadores para exibição no mapa
    markers = []
    for species in species_data:
        name, lat, lon, _ = species
        try:
            lat = float(lat)
            lon = float(lon)
            
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                markers.append({
                    "lat": lat,
                    "lon": lon,
                    "popup": f"<b>{name}</b>"  # O conteúdo do popup (nome da espécie)
                })
            else:
                st.warning(f"Invalid coordinates for species: {name} (Lat: {lat}, Lon: {lon})")
        except ValueError:
            st.warning(f"Invalid latitude or longitude for species: {name} (Lat: {lat}, Lon: {lon})")

    # Exibindo o mapa com os marcadores usando streamlit-leaflet
    st_leaflet(markers=markers, center=(species_data[0][1], species_data[0][2]), zoom=5)

# Chama a função para exibir o mapa com as espécies
display_map()
