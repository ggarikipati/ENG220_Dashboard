# -*- coding: utf-8 -*-
# Group 004 - Water Data in New Mexico Districts

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Title of the app
#st.title("Group-004")

st.markdown("""
### Water Data in New Mexico Districts

This project explores environmental and climatic data across various **districts in New Mexico**, using datasets from both local and regional sources.  
The goal is to understand the environmental challenges and trends affecting different areas, with a focus on **state and local government policies** related to water conservation.  

We examine the **effectiveness of conservation strategies**, public awareness initiatives, and **technological innovations** in water management.  
Through this analysis, we aim to identify best practices and offer recommendations to strengthen water conservation and promote **sustainable environmental management**.
""")

# Load district map image (optional)
image_path = os.path.join(os.path.dirname(__file__), "WaterDistricts.png")
if os.path.exists(image_path):
    st.image(image_path, caption="Water Districts in New Mexico")

# Locate script directory and district folders
base_path = os.path.dirname(__file__)
district_folders = [f"District {i}" for i in range(1, 8)]
available_folders = [folder for folder in district_folders if os.path.exists(os.path.join(base_path, folder))]

if not available_folders:
    st.error("No district folders found in the current directory.")
else:
    selected_district = st.selectbox("Select a District", available_folders)
    folder_path = os.path.join(base_path, selected_district)

    # List CSV files
    csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

    if not csv_files:
        st.warning(f"No CSV files found in {selected_district}.")
    else:
        selected_file = st.selectbox("Select a CSV File", csv_files)
        file_path = os.path.join(folder_path, selected_file)

        try:
            # Load and preprocess CSV data
            raw_data = pd.read_csv(file_path, header=1)
            raw_data.rename(columns={raw_data.columns[0]: "Timestamp"}, inplace=True)
            raw_data['Timestamp'] = pd.to_datetime(raw_data['Timestamp'], errors='coerce')
            raw_data.dropna(subset=['Timestamp'], inplace=True)
            raw_data.replace("NR", "none", inplace=True)

            numeric_columns = raw_data.columns[1:]
            for col in numeric_columns:
                raw_data[col] = pd.to_numeric(raw_data[col], errors='coerce')

            # Aggregate by day
            daily_data = raw_data.set_index('Timestamp').resample('D').mean().reset_index()
            non_numeric = raw_data.set_index('Timestamp').resample('D').first().reset_index()
            for col in non_numeric.columns:
                if col not in daily_data.columns:
                    daily_data[col] = non_numeric[col]

            # Show data
            st.subheader(f"Data Preview: {selected_district} - {selected_file}")
            st.dataframe(daily_data)

            # Column selectors
            columns = daily_data.columns.tolist()
            x_column = st.selectbox("Select X-axis column", columns, index=0)
            y_column = st.selectbox("Select Y-axis column", columns[1:], index=0)

            graph_type = st.selectbox("Select Graph Type", ["Line", "Scatter", "Bar"])

            # Plot graph
            if st.button("Plot Graph"):
                fig, ax = plt.subplots()

                if graph_type == "Line":
                    ax.plot(daily_data[x_column], daily_data[y_column], marker='o')
                    ax.set_title(f"{y_column} vs {x_column} (Line Plot)")

                elif graph_type == "Scatter":
                    ax.scatter(daily_data[x_column], daily_data[y_column])
                    ax.set_title(f"{y_column} vs {x_column} (Scatter Plot)")

                elif graph_type == "Bar":
                    ax.bar(daily_data[x_column], daily_data[y_column])
                    ax.set_title(f"{y_column} vs {x_column} (Bar Chart)")

                ax.set_xlabel(x_column)
                ax.set_ylabel(y_column)
                st.pyplot(fig)

            st.info("Tip: Data has been aggregated to one point per day for better performance.")

        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
