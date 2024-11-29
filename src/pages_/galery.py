import streamlit as st
import sqlite3
import plotly.express as px
import pandas as pd
from db_utils.dbutils import fetch_species_with_location

st.title('Mapa')

def display_map():
    """Função para exibir o mapa com os marcadores de espécies"""
    species_data = fetch_species_with_location()

    if not species_data:
        st.warning("No species data available with location.")
        return

    # Convertendo os dados para um DataFrame do Pandas para usar com Plotly
    df = pd.DataFrame(species_data, columns=["name", "latitude", "longitude", "image_path"])

    # Criando o mapa interativo com Plotly
    fig = px.scatter_map(df,
                         lat='latitude', 
                         lon='longitude', 
                         hover_name='name') 
    
    fig.update_layout(map_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Exibindo o mapa interativo no Streamlit
    st.plotly_chart(fig)

