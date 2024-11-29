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
        'Pages', ['Main', 'Map']
        )
    pages_main = {
        'Main': main_page,
        'Map': galery,

    }

    pages_main[page_selection]()


def main_page():
    init_db()  # Ensures the database and table are created

    with st.form("Cadastro do Animal"):
        st.write("Upload")
        uploaded_img = st.file_uploader('Image')

        name = st.text_input('Nome do Animal')
        date = st.date_input("Date", datetime.date(2024, 11, 29))
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

def galery():
    return display_map()

main()
if __name__=='__main__':
    main()
