import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Edit Vendor Areas in Google Sheets")

# Function to initialize the Google Sheets connection
def initialize_connection():
    return st.connection("gsheets", type=GSheetsConnection)

# Function to fetch the latest data from Google Sheets
def fetch_latest_data(conn):
    return conn.read(worksheet="Names")

# Check if session state exists for the connection
if "conn" not in st.session_state:
    st.session_state["conn"] = initialize_connection()

# Reinitialize the connection explicitly
conn = st.session_state["conn"]

# Fetch the latest data
existing_data = fetch_latest_data(conn)

st.subheader("Edit Vendor Area")
if not existing_data.empty:
    # Display and allow editing of the 'area' column
    edited_data = st.data_editor(
        existing_data,
        column_config={
            "area": st.column_config.SelectboxColumn(
                label="Select Area",
                width="medium",
                options=[
                    "Production",
                    "Education",
                    "Community",
                    "Emergency",
                    "Agriculture",
                ],
                required=True,
            )
        },
        hide_index=True,
        disabled=["CompanyName", "BusinessType", "Products", "YearsInBusiness", "OnboardingDate", "AdditionalInfo"],  # Disable other columns
        key="data_editor"
    )

    # Compare the original and edited data to detect changes
    if not edited_data.equals(existing_data):
        # Update Google Sheets with the new data
        conn.update(worksheet="Names", data=edited_data)
        
        # Reinitialize the connection and fetch updated data
        st.session_state["conn"] = initialize_connection()
        
        # Trigger rerun to re-fetch and reinitialize
        st.rerun()
else:
    st.write("No data available to display.")
