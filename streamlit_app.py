import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Edit Vendor Areas in Google Sheets")

conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="Names")
st.dataframe(existing_data)
