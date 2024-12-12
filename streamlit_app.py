import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Edit Vendor Areas in Google Sheets")

# Initialize Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Function to fetch the latest data from Google Sheets
def fetch_latest_data():
    return conn.read(worksheet="Names")

# Initial fetch of data
existing_data = fetch_latest_data()

# Display and allow editing of the 'area' column only
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
        disabled=["CompanyName", "BusinessType", "Products", "YearsInBusiness", "OnboardingDate", "AdditionalInfo"]  # Disable other columns
    )

    # Compare the original and edited data to detect changes
    if not edited_data.equals(existing_data):
        # Update Google Sheets with the new data
        conn.update(worksheet="Names", data=edited_data)
        
        # Re-fetch the updated data from Google Sheets
        updated_data = fetch_latest_data()

        # Reinitialize `st.data_editor` with the updated data
        st.rerun()
else:
    st.write("No data available to display.")
