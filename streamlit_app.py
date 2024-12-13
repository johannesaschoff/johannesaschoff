import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Edit Vendor Areas in Google Sheets")

# Fetch data directly without caching
def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(worksheet="Names")

existing_data = fetch_data()
st.dataframe(existing_data)
