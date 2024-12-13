import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Edit Vendor Areas in Google Sheets")

# Use caching with a TTL to refresh data periodically
@st.cache_data(ttl=60)  # Refresh data every 60 seconds
def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(worksheet="Names")

# Fetch and display data
existing_data = fetch_data()
st.dataframe(existing_data)
