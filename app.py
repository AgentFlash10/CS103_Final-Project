import streamlit as st
import pandas as pd

st.title("Daw Mabalda ta haw")

# File Upload
uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Check the file type and load accordingly
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    st.write("Data Preview", df.head(30))  # Show first 30 rows initially

# Data Deduplication and Cleansing: Handle missing values, null values, and irrelevant data
    if st.button("Clean and Deduplicate Data"):
        # Remove duplicates
        df = df.drop_duplicates()

        # Handle missing values: Fill missing data with 0
        df.fillna(0, inplace=True)

        # Handle null values by dropping them
        df.dropna(inplace=True)

        # Remove irrelevant data: Rows with zero or negative 'Amount'
        if 'Amount' in df.columns:
            df = df[df['Amount'] > 0]

        st.write("Data After Cleansing and Deduplication", df.head(30))  # Show first 30 rows after cleansing