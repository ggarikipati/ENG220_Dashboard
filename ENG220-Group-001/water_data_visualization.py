# -*- coding: utf-8 -*-
# Code to generate an app interface in streamlit intaking a csv data file and showing various graphs

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("Water Supply Data Visualization App")

debug = 1

#if uploaded_file is not None:
if debug == 1:
    # Read the CSV file
    data = pd.read_csv('nm_water_weather_data.csv')

    st.markdown('<p style="color:blue; font-size:30px;">Data Preview</p>', unsafe_allow_html=True)

    st.dataframe(data)

    # Dropdown for selecting columns
    columns = data.columns.tolist()
    x_column = st.selectbox("Select X-axis column", columns)
    y_column = st.selectbox("Select Y-axis column", columns)

    # Dropdown for graph type
    graph_type = st.selectbox(
        "Select Graph Type",
        ["Line", "Scatter", "Bar"]
    )

    # Plot button
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

else:
    st.info("Please upload a CSV file to get started.")
