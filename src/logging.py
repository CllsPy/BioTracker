import sqlite3
import datetime
import streamlit as st
import os

from db_utils.dbutils import init_db
from db_utils.dbutils import add_species
from pages_.galery import display_map

def main():
    st.sidebar.title('Navbar')
    page_selection = st.sidebar.selectbox(
        '', ['Main', 'Map']
        )

    pages_main = {
        'Main': main_page,
        'Map': galery,

    }

    pages_main[page_selection]()


def main_page():
    init_db()  # Ensures the database and table are created

    with st.form("Report"):
        #st.write("Upload")
        st.subheader('Cadastro do Animal')
        uploaded_img = st.file_uploader('Picture')

        name = st.selectbox(
            'Specie', 
            [
                'Panthera onca', 
                'Chrysocyon brachyurus', 
                'Ailuropoda melanoleuca',
                'Balaenoptera physalus'
                ]
            )

        date = st.date_input("Date", datetime.date(2024, 11, 29))

        col1, col2 = st.columns(2)

        lat = col1.text_input('latitude')
        lon = col2.text_input('longitude')

        submitted = st.form_submit_button("Report")
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

def galery():
    return display_map()

if __name__=='__main__':
    main()
