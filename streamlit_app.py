import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Edit Vendor Areas in Google Sheets")

# Initialize Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="Names")

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

    # Button to save changes to Google Sheets
    if st.button("Save Changes"):
        conn.update(worksheet="Names", data=edited_data)
        st.session_state["reload_trigger"] = True  # Set reload trigger in session state
        st.experimental_set_query_params(reload="true")  # Update query params for a soft reload

else:
    st.write("No data available to display.")

# Check for reload trigger
if "reload_trigger" in st.session_state:
    del st.session_state["reload_trigger"]  # Clear the trigger to avoid infinite reload loop
    st.experimental_rerun()  # Safely reload
