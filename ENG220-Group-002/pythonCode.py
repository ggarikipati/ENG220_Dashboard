# -*- coding: utf-8 -*-
# Group 002 Streamlit Visualization App

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Title of the app
st.title("Group-002")

st.markdown("""
### Water Quality Trends in New Mexico (2020–2023)

This project analyzes water quality reports across the state of **New Mexico**, focusing on data collected between **2020 and 2023**.  
We examine contaminant levels over time to understand how water quality is changing and whether it's improving or declining.  
Through this trend analysis, we aim to identify potential contributing variables and actions that lead to improved water quality outcomes across the state.
""")

try:
    # Read CSV relative to this script's directory
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, 'Water_Data_Clean1.csv')
    data = pd.read_csv(csv_path)

    st.subheader("Data Preview")
    st.dataframe(data)

    # Dropdown for selecting columns
    columns = data.columns.tolist()
    x_column = st.selectbox("Select X-axis column", columns)
    y_column = st.selectbox("Select Y-axis column", columns)

    # Dropdown for graph type
    graph_type = st.selectbox("Select Graph Type", ["Line", "Scatter", "Bar", "Pie"])

    # Plot button
    if st.button("Plot Graph"):
        fig, ax = plt.subplots()

        if graph_type == "Line":
            ax.plot(data[x_column], data[y_column], marker='o')
            ax.set_title(f"{y_column} vs {x_column} (Line Plot)")
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            st.pyplot(fig)

        elif graph_type == "Scatter":
            ax.scatter(data[x_column], data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Scatter Plot)")
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            st.pyplot(fig)

        elif graph_type == "Bar":
            ax.bar(data[x_column], data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Bar Chart)")
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            st.pyplot(fig)

        elif graph_type == "Pie":
            if len(data[x_column].unique()) <= 10:
                pie_labels = data[x_column].astype(str)
                pie_values = data[y_column]
                fig, ax = plt.subplots()
                ax.pie(
                    pie_values,
                    labels=pie_labels,
                    autopct='%1.1f%%',
                    startangle=90
                )
                ax.set_title(f"{y_column} Distribution (Pie Chart)")
                st.pyplot(fig)
            else:
                st.error("Pie chart requires fewer than 10 unique categories in the X-axis.")

    st.info("Tip: Ensure selected columns are numeric for meaningful plots.")

except FileNotFoundError:
    st.error("CSV file not found. Please ensure 'Water_Data_Clean1.csv' is placed in the same directory as this script.")
