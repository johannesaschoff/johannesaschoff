import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Manage Vendors in Google Sheets")

# Initialize Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="Names")

# Display the current dataframe
st.subheader("Existing Vendor Data")
if not existing_data.empty:
    st.dataframe(existing_data)
else:
    st.write("No data available yet.")

# BUSINESS TYPES and PRODUCTS lists
BUSINESS_TYPES = [
    "Manufacturer",
    "Distributor",
    "Wholesaler",
    "Retailer",
    "Service Provider",
]

PRODUCTS = [
    "Electronics",
    "Apparel",
    "Groceries",
    "Software",
    "Other",
]

# Form to add or update vendor data
with st.form(key="vendor_form"):
    st.subheader("Add or Update Vendor Details")
    company_name = st.text_input(label="Company Name*")
    business_type = st.selectbox("Business Type*", options=BUSINESS_TYPES, index=None)
    products = st.multiselect("Products Offered", options=PRODUCTS)
    years_in_business = st.slider("Years in Business", 0, 50, 5)
    onboarding_date = st.date_input(label="Onboarding Date")
    additional_info = st.text_area(label="Additional Notes")
    
    st.markdown("**Fields marked with * are required**")
    submit_button = st.form_submit_button(label="Submit Vendor Details")

    if submit_button:
        # Validate required fields
        if not company_name or not business_type:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()

        # Check if company already exists in the data
        if "CompanyName" in existing_data.columns:
            existing_index = existing_data[existing_data["CompanyName"] == company_name].index
        else:
            existing_index = pd.Index([])

        # Prepare the new or updated row
        vendor_data = pd.DataFrame(
            [
                {
                    "CompanyName": company_name,
                    "BusinessType": business_type,
                    "Products": ", ".join(products),
                    "YearsInBusiness": years_in_business,
                    "OnboardingDate": onboarding_date.strftime("%Y-%m-%d"),
                    "AdditionalInfo": additional_info,
                }
            ]
        )

        if not existing_index.empty:
            # Update existing row
            existing_data.loc[existing_index[0]] = vendor_data.iloc[0]
            st.success("Vendor details successfully updated!")
        else:
            # Append new row
            existing_data = pd.concat([existing_data, vendor_data], ignore_index=True)
            st.success("Vendor details successfully submitted!")

        # Save updated dataframe to Google Sheets
        conn.update(worksheet="Names", data=existing_data)
        st.experimental_rerun()  # Reload the app to reflect the updated dataframe
