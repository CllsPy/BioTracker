from db_utils import add_species, fetch_species, init_db
import datetime

from db_utils import init_db
init_db()  # Ensures the database and table are created

import streamlit as st

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
        add_species(name, date, lon, lat, '/path')
        