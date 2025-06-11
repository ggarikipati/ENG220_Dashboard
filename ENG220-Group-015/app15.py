import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set current directory and file path
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'HealthData.csv')

# App Title
#st.title("Group-015")

# Project Introduction
st.markdown("""
### Health Care Access Across New Mexico Counties

Our group's project focuses on **health care access across different counties in New Mexico**.  
We analyze and compare factors such as clinical care, life expectancy, uninsured population percentage, and quality of life indicators.  
The dataset combines and averages all available information from **2010 to 2023**, helping to identify disparities and potential areas for policy improvement.

""")

# Load CSV
try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("The file 'HealthData.csv' was not found. Please ensure the file is placed in the correct directory.")
    data = None

if data is not None:
    st.write("### Data Preview")
    st.dataframe(data)

    columns = data.columns.tolist()
    x_column = st.selectbox("Select X-axis column", columns)
    y_column = st.selectbox("Select Y-axis column", columns)

    graph_type = st.selectbox("Select Graph Type", ["Line", "Scatter", "Bar", "Pie"])

    if st.button("Plot Graph"):
        fig, ax = plt.subplots()

        if graph_type != "Pie":
            # Ensure Y is numeric
            if pd.api.types.is_numeric_dtype(data[y_column]):
                y_min, y_max = data[y_column].min(), data[y_column].max()
                padding = (y_max - y_min) * 0.1
                y_min -= padding
                y_max += padding
            else:
                st.error("Y-axis column must be numeric for plotting.")
                st.stop()

        if graph_type == "Line":
            ax.plot(data[x_column], data[y_column], marker='o')
            ax.set_title(f"{y_column} vs {x_column} (Line Plot)")
            plt.xticks(rotation=90)
            ax.set_ylim(y_min, y_max)

        elif graph_type == "Scatter":
            ax.scatter(data[x_column], data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Scatter Plot)")
            plt.xticks(rotation=90)
            ax.set_ylim(y_min, y_max)

        elif graph_type == "Bar":
            ax.bar(data[x_column], data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Bar Chart)")
            plt.xticks(rotation=90)
            ax.set_ylim(y_min, y_max)

        elif graph_type == "Pie":
            if len(data[x_column].unique()) <= 35:
                pie_data = data.groupby(x_column)[y_column].sum()
                plt.pie(
                    pie_data,
                    labels=pie_data.index,
                    autopct='%1.1f%%',
                    startangle=90
                )
                plt.title(f"{y_column} Distribution (Pie Chart)")
            else:
                st.error("Too many categories for pie chart. Try a different graph type.")

        if graph_type != "Pie":
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            st.pyplot(fig)
        else:
            st.pyplot(plt)

    st.write("Tip: Ensure the selected columns are numeric for meaningful plots.")
else:
    st.info("Please upload a CSV file to get started.")
