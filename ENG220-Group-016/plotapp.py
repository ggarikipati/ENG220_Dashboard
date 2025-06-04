import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set up file path using os
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'Suicide Deaths by County, New Mexico, 2016-2020.csv')

# App Title
st.title("Group-016")

# Project Summary
st.markdown("""
### Suicide Deaths in New Mexico Counties

This project analyzed suicide death data across New Mexico counties to identify areas at higher risk.  
Key findings reveal disparities across counties—**Catron County** recorded the highest suicide rate in the contiguous U.S. from 2010–2020.  
Other notable counties include **San Juan, McKinley, and Bernalillo**.  
While rural counties often show **higher rates**, larger counties (Bernalillo, Santa Fe, Doña Ana) contribute the **highest absolute counts**.  
This analysis aims to support targeted **suicide prevention** strategies and more **equitable resource allocation** across New Mexico.

""")

# Load CSV
try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("The file was not found. Please ensure it is in the correct folder.")
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

        if graph_type == "Line":
            ax.plot(data[x_column], data[y_column], marker='o')
            ax.set_title(f"{y_column} vs {x_column} (Line Plot)")

        elif graph_type == "Scatter":
            ax.scatter(data[x_column], data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Scatter Plot)")

        elif graph_type == "Bar":
            ax.bar(data[x_column], data[y_column])
            ax.set_title(f"{y_column} vs {x_column} (Bar Chart)")

        elif graph_type == "Pie":
            if len(data[x_column].unique()) <= 10:
                plt.pie(
                    data[y_column],
                    labels=data[x_column],
                    autopct='%1.1f%%',
                    startangle=90
                )
                plt.title(f"{y_column} (Pie Chart)")
            else:
                st.error("Too many categories for a pie chart. Try a different graph type.")

        if graph_type != "Pie":
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            st.pyplot(fig)
        else:
            st.pyplot(plt)

    st.write("Tip: Ensure the selected columns are numeric for meaningful plots.")
else:
    st.info("CSV file not available. Please ensure it's uploaded or exists in the correct directory.")
