import streamlit as st
import pandas as pd

st.title("Daw Mabalda ta haw")

# File Upload
uploaded_file = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Load the data
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview", df.head())

    # Data Deduplication
    if st.checkbox("Remove Duplicates"):
        df = df.drop_duplicates()
        st.write("Deduplicated Data", df.head())

    # Data Cleansing: Handle missing values
    if st.checkbox("Clean Missing Values"):
        fill_value = st.selectbox("Choose Fill Value", ["None", "Mean", "Zero"])
        if fill_value == "Mean":
            df.fillna(df.mean(), inplace=True)
        elif fill_value == "Zero":
            df.fillna(0, inplace=True)
        st.write("Data After Filling Missing Values", df.head())

    # Remove irrelevant data: Rows with zero or negative 'Amount'
    if st.checkbox("Remove Irrelevant Data (Zero or Negative Amounts)"):
        df = df[df['Amount'] > 0]
        st.write("Data After Removing Irrelevant Rows", df.head())