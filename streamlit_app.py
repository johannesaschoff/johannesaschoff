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
        st.success("Changes saved successfully!")
        st.experimental_rerun()  # Reload the app to reflect updates
else:
    st.write("No data available to display.")
