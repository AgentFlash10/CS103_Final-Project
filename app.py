import streamlit as st
import pandas as pd

st.title("CS103 Final Project")

# File Upload, allow multiple file uploads
uploaded_files = st.file_uploader("Upload your datasets", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Check the file type and load accordingly
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)

        st.write(f"Data Preview for {uploaded_file.name}", df.head(30))  #Show first 30 rows initially

        # Data Deduplication and Cleansing: Handle missing values null values and irrelevant data
        if st.button(f"Clean and Deduplicate Data for {uploaded_file.name}"):
            # Remove duplicates
            df = df.drop_duplicates()

            # Handle missing values: Fill missing data with 0
            df.fillna(0, inplace=True)

            # Handle null values by dropping them
            df.dropna(inplace=True)

            # Remove rows where any numeric column has less than 0
            numeric_cols = df.select_dtypes(include=['number']).columns
            df = df[(df[numeric_cols] >= 0).all(axis=1)]

            st.write(f"Data After Cleansing and Deduplication for {uploaded_file.name}", df.head(30))  #Show first 30 rows after cleansing