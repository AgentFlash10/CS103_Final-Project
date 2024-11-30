import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("CS103 Final Project")

# Initialize an empty list to store datasets and their names
dfs = []
processed_dfs = {}

# File Upload: Allow multiple file uploads
uploaded_files = st.file_uploader("Upload your datasets", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Load data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)

        # Add dataset to the list
        dfs.append((uploaded_file.name, df))

        # Display uploaded data
        st.write(f"Dataset: {uploaded_file.name}")
        st.write(df)

    # Sidebar for selecting datasets
    st.sidebar.title("Data Operations")
    dataset_options = [name for name, _ in dfs]

    if len(dataset_options) > 1:
        selected_datasets = st.sidebar.multiselect("Select Datasets for Operations", dataset_options, default=dataset_options)
    else:
        selected_datasets = dataset_options

    # Perform operations only if datasets are selected
    if selected_datasets:
        # Data Deduplication
        if st.sidebar.checkbox("Data Deduplication"):
            for dataset_name in selected_datasets:
                st.subheader(f"Data Deduplication for {dataset_name}")
                df = next(df for name, df in dfs if name == dataset_name)
                dedup_df = df.drop_duplicates()
                st.write("Deduplicated Data:")
                st.write(dedup_df)

                # Store processed data
                processed_dfs[dataset_name] = dedup_df

        # Data Cleansing
        if st.sidebar.checkbox("Data Cleansing"):
            for dataset_name in selected_datasets:
                st.subheader(f"Data Cleansing for {dataset_name}")
                df = processed_dfs.get(dataset_name, next(df for name, df in dfs if name == dataset_name))
                
                # Fill missing values with 0
                filled_df = df.fillna(0)
                        
                # Replace negative values with 0
                numeric_cols = filled_df.select_dtypes(include=['number']).columns
                filled_df[numeric_cols] = filled_df[numeric_cols].clip(lower=0)
                        
                st.write("Cleansed Data:")
                st.write(filled_df)

                # Store processed data
                processed_dfs[dataset_name] = filled_df

        # Format Revision
        if st.sidebar.checkbox("Format Revision"):
            for dataset_name in selected_datasets:
                st.subheader(f"Format Revision for {dataset_name}")
                df = processed_dfs.get(dataset_name, next(df for name, df in dfs if name == dataset_name))
                
                # Display original data types
                st.write("Original Data Types:")
                st.write(df.dtypes)

                column_to_convert = st.selectbox(f"Select column to change data type ({dataset_name})", df.columns, key=f"convert_{dataset_name}")
                data_type = st.selectbox(f"Select target data type ({dataset_name})", ["int", "float", "str", "datetime"], key=f"type_{dataset_name}")
                
                if st.button(f"Convert Column for {dataset_name}", key=f"convert_btn_{dataset_name}"):
                    try:
                        # Show the original data type of the selected column
                        original_dtype = df[column_to_convert].dtype
                        st.write(f"Original Data Type of {column_to_convert}: {original_dtype}")

                        # Perform conversion based on selected type
                        if data_type == "int":
                            df[column_to_convert] = pd.to_numeric(df[column_to_convert], errors="coerce").astype("Int64")
                        elif data_type == "float":
                            df[column_to_convert] = pd.to_numeric(df[column_to_convert], errors="coerce")
                        elif data_type == "str":
                            df[column_to_convert] = df[column_to_convert].astype(str)
                        elif data_type == "datetime":
                            df[column_to_convert] = pd.to_datetime(df[column_to_convert], errors="coerce")

                        # Show updated data type of the selected column
                        updated_dtype = df[column_to_convert].dtype
                        st.write(f"Updated Data Type of {column_to_convert}: {updated_dtype}")
                        
                    except Exception as e:
                        st.error(f"Error: {e}")

        # Merging/Joining
        if len(dfs) > 1 and st.sidebar.checkbox("Merge Datasets"):
            st.subheader("Merge Datasets")
            dataset1 = st.selectbox("Select First Dataset", dataset_options, key="merge_dataset1")
            dataset2 = st.selectbox("Select Second Dataset", [name for name in dataset_options if name != dataset1], key="merge_dataset2")
            df1 = processed_dfs.get(dataset1, next(df for name, df in dfs if name == dataset1))
            df2 = processed_dfs.get(dataset2, next(df for name, df in dfs if name == dataset2))
            join_column1 = st.selectbox(f"Select join column from {dataset1}", df1.columns)
            join_column2 = st.selectbox(f"Select join column from {dataset2}", df2.columns)
            join_method = st.selectbox("Select join method", ["inner", "left", "right", "outer"])
            if st.button("Merge Datasets"):
                try:
                    merged_df = pd.merge(df1, df2, how=join_method, left_on=join_column1, right_on=join_column2)
                    st.write(merged_df)
                except Exception as e:
                    st.error(f"Error: {e}")

        # Data Derivation
        if st.sidebar.checkbox("Data Derivation"):
            for dataset_name in selected_datasets:
                st.subheader(f"Data Derivation for {dataset_name}")
                df = processed_dfs.get(dataset_name, next(df for name, df in dfs if name == dataset_name))
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                if len(numeric_cols) < 2:
                    st.warning("Not enough numeric columns to perform derivation.")
                else:
                    col1 = st.selectbox(f"Select first column ({dataset_name})", numeric_cols, key=f"{dataset_name}_col1")
                    col2 = st.selectbox(f"Select second column ({dataset_name})", numeric_cols, key=f"{dataset_name}_col2")
                    operation = st.selectbox("Select operation", ["Add", "Subtract", "Multiply", "Divide"])
                    if st.button(f"Apply Derivation on {dataset_name}"):
                        try:
                            new_col_name = f"{col1}_{operation.lower()}_{col2}"
                            if operation == "Add":
                                df[new_col_name] = df[col1] + df[col2]
                            elif operation == "Subtract":
                                df[new_col_name] = df[col1] - df[col2]
                            elif operation == "Multiply":
                                df[new_col_name] = df[col1] * df[col2]
                            elif operation == "Divide":
                                df[new_col_name] = df[col1] / df[col2].replace(0, float('nan'))
                            st.write(df)
                        except Exception as e:
                            st.error(f"Error: {e}")

        # Data Aggregation
        if st.sidebar.checkbox("Data Aggregation"):
            for dataset_name in selected_datasets:
                st.subheader(f"Data Aggregation for {dataset_name}")
                df = processed_dfs.get(dataset_name, next(df for name, df in dfs if name == dataset_name))
                group_by_col = st.selectbox(f"Select a column to group by ({dataset_name})", df.columns, key=f"groupby_{dataset_name}")
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                agg_cols = st.multiselect(f"Select columns to aggregate ({dataset_name})", numeric_cols, key=f"aggcols_{dataset_name}")
                agg_funcs = st.multiselect("Select aggregation functions", ["sum", "mean", "min", "max"])
                if st.button(f"Perform Aggregation for {dataset_name}"):
                    if not agg_cols or not agg_funcs:
                        st.warning("Please select at least one column and one aggregation function.")
                    else:
                        agg_dict = {col: agg_funcs for col in agg_cols}
                        aggregated_df = df.groupby(group_by_col).agg(agg_dict).reset_index()
                        st.write(aggregated_df)

        # Descriptive Statistics
        if st.sidebar.checkbox("Descriptive Statistics"):
            for dataset_name in selected_datasets:
                st.subheader(f"Descriptive Statistics for {dataset_name}")
                df = processed_dfs.get(dataset_name, next(df for name, df in dfs if name == dataset_name))
                st.write(df.describe())

        # Data Visualization
        if st.sidebar.checkbox("Data Visualization"):
            for dataset_name in selected_datasets:
                st.subheader(f"Data Visualization for {dataset_name}")
                df = processed_dfs.get(dataset_name, next(df for name, df in dfs if name == dataset_name))
                
                # Select chart type
                chart_type = st.selectbox(f"Select chart type ({dataset_name})", ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Count Plot", "Pie Chart"])
                
                # Separate numeric and non-numeric columns
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                non_numeric_cols = df.select_dtypes(exclude=['number']).columns.tolist()
                
                if chart_type in ["Bar Chart", "Line Chart", "Histogram"]:
                    if numeric_cols:
                        column = st.selectbox(f"Select column to visualize ({dataset_name})", numeric_cols)
                    else:
                        st.warning(f"No numeric columns available for {chart_type}. Please choose another chart.")
                elif chart_type == "Scatter Plot":
                    if len(numeric_cols) >= 2:
                        x_col = st.selectbox(f"Select X-axis column ({dataset_name})", numeric_cols)
                        y_col = st.selectbox(f"Select Y-axis column ({dataset_name})", numeric_cols)
                    else:
                        st.warning(f"Not enough numeric columns for scatter plot in {dataset_name}.")
                elif chart_type == "Count Plot":
                    if non_numeric_cols:
                        column = st.selectbox(f"Select categorical column to visualize ({dataset_name})", non_numeric_cols)
                    else:
                        st.warning("No non-numeric columns available for count plot.")
                elif chart_type == "Pie Chart":
                    if non_numeric_cols:
                        column = st.selectbox(f"Select categorical column to visualize ({dataset_name})", non_numeric_cols)
                    else:
                        st.warning("No non-numeric columns available for pie chart.")
                
                # Generate the selected chart
                if st.button(f"Generate {chart_type} for {dataset_name}"):
                    fig, ax = plt.subplots()
                    try:
                        if chart_type == "Bar Chart":
                            df[column].value_counts().plot(kind='bar', ax=ax)
                        elif chart_type == "Line Chart":
                            ax.plot(df.index, df[column])
                        elif chart_type == "Scatter Plot":
                            sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax)
                        elif chart_type == "Histogram":
                            df[column].plot(kind='hist', bins=20, ax=ax)
                        elif chart_type == "Count Plot":
                            sns.countplot(data=df, x=column, ax=ax)
                        elif chart_type == "Pie Chart":
                            df[column].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
                        
                        st.pyplot(fig)
                    except Exception as e:
                        st.error(f"Error: {e}")