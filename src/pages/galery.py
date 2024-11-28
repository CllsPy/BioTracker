import streamlit as st
import sqlite3
import plotly.express as px
import pandas as pd

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

# Função para exibir o mapa com os marcadores de espécies
def display_map():
    species_data = fetch_species_with_location()

    if not species_data:
        st.write("No species data available with location.")
        return

    # Convertendo os dados para um DataFrame do Pandas para usar com Plotly
    df = pd.DataFrame(species_data, columns=["name", "latitude", "longitude", "image_path"])

    # Criando o mapa interativo com Plotly
    fig = px.scatter_geo(df, 
                         lat='latitude', 
                         lon='longitude', 
                         hover_name='name', 
                         title="Espécies no Mapa",
                         template='plotly',  # Você pode escolher o template que mais gosta
                         projection="natural earth")  # Você pode escolher outros tipos de projeção

    # Exibindo o mapa interativo no Streamlit
    st.plotly_chart(fig)

# Chama a função para exibir o mapa com as espécies
display_map()
