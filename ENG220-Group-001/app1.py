# -*- coding: utf-8 -*-
# Code to generate an app interface in streamlit intaking a csv data file and showing various graphs

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Title of the app
#st.title("Group-001")

st.markdown("""
### Water Supply Data Visualization App

This dashboard explores the relationship between water supply, water return, and weather patterns in **Albuquerque and Bernalillo County**.  
We compare municipal water data with average weather conditions to uncover potential correlations.  
The data used in this project was sourced from **USGS**, **ABCWUA**, and the **National Weather Service (NWS)**.
""")

debug = 1

if debug == 1:
    try:
        # Load the data using path relative to the script location
        current_dir = os.path.dirname(__file__)
        csv_path = os.path.join(current_dir, 'nm_water_weather_data.csv')
        data = pd.read_csv(csv_path)

        st.subheader("Data Preview")
        st.dataframe(data)

        # Dropdowns for selecting columns
        columns = data.columns.tolist()
        x_column = st.selectbox("Select X-axis column", columns)
        y_column = st.selectbox("Select Y-axis column", columns)

        # Dropdown for graph type
        graph_type = st.selectbox("Select Graph Type", ["Line", "Scatter", "Bar"])

        # Plot
        if st.button("Plot Graph"):
            fig, ax = plt.subplots()

            if graph_type == "Line":
                ax.plot(data[x_column], data[y_column], marker='o')
                ax.set_title(f"{y_column} vs {x_column} (Line Plot)")

            elif graph_type == "Scatter":
                ax.scatter(data[x_column], data[y_column])
                ax.set_title(f"{y_column} vs {x_column} (Scatter Plot)")

            elif graph_type == "Bar":
                ax.bar(data[x_column], data[y_column])
                ax.set_title(f"{y_column} vs {x_column} (Bar Chart)")

            st.pyplot(plt)

        st.markdown('<p style="color:red; font-size:20px;">Tip: Ensure the selected columns are numeric for meaningful plots.</p>', unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("CSV file not found. Please check the path and try again.")
else:
    st.info("Please upload a CSV file to get started.")
