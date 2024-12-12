import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Read Google Sheet as DataFrame")

conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="Names")

#st.dataframe(existing_data)

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
    "Groceries"
    "Software"
    "Other"
]

with st.form(key="vendor_form"):
    company_name = st.text_input(label="Company Name*")
    business_type = st.selectbox("Business Type*", options=BUSINESS_TYPES, index=None)
    products = st.multiselect("Products Offered", options=PRODUCTS)
    years_in_business = st.slider("Years in Business", 0, 50, 5)
    onboarding_date = st.date_input(label="Onboarding Date")
    additional_info = st.text_area(label="Additional Notes")
    
    st.markdown ("**required*")
    submit_button = st.form_submit_button(label="Submit Vendor Details")

    if submit_button:
        if submit_button:
            # Check if all mandatory fields are filled
            if not company_name or not business_type:
                st.warning("Ensure all mandatory fields are filled.")
                st.stop()
            elif existing_data["CompanyName"].str.contains(company_name).any():
                st.warning("A vendor with this company name already exists.")
                st.stop ()
            else:
                # Create a new row of vendor data
                vendor_data = pd.DataFrame(
                    [
                        {
                            "CompanyName" : company_name,
                            "BusinessType": business_type,
                            "Products": ", ".join(products),
                            "YearsInBusiness": years_in_business,
                            "OnboardingDate": onboarding_date.strftime("%Y-%m-%d"),
                            "Additionallnfo": additional_info,
                        }
                    ]   
                )

                updated_df = pd.concat([existing_data, vendor_data], ignore_index = True)
                conn.update(worksheet="Names", data=updated_df)
                st.success("Vendor details successfully submitted!")
                    