import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Edit Vendor Areas in Google Sheets")

# Initialize Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Read data from Google Sheets
existing_data = conn.read(worksheet="Names")

# Always reset session state on reload to load actual values
if "previous_data" not in st.session_state or st.session_state.get("reload", False):
    st.session_state["previous_data"] = existing_data.copy()
    st.session_state["reload"] = False  # Reset reload flag

# Display and allow editing of the 'area' column only
st.subheader("Edit Vendor Area")
if not existing_data.empty:
    # Allow editing only for the 'area' column
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

    # Check if any changes were made to the dataframe
    if not edited_data.equals(st.session_state["previous_data"]):
        # Update Google Sheets with the new data
        conn.update(worksheet="Names", data=edited_data)
        st.session_state["previous_data"] = edited_data.copy()  # Update session state
        st.session_state["reload"] = True  # Set reload flag
        st.success("Changes saved successfully!")
        st.rerun()  # Automatically reload to reflect updates
else:
    st.write("No data available to display.")
