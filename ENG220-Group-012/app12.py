import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set current directory
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'gunarchieve_cleaned_team12.csv')

# Title of the app
st.title("Group-012")

st.markdown("""
### Gun Violence Archive Data Exploration

This project visualizes data from the **Gun Violence Archive**, offering insights into patterns and frequency of gun-related incidents in the United States.  
Users can explore variables such as **incident dates**, **locations**, **victim counts**, and other dimensions to better understand gun violence trends.

---
""")

# Load the CSV data
try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("CSV file not found. Please ensure the file is placed correctly.")
    data = None

if data is not None:
    st.write("### Data Preview")
    st.dataframe(data)

    # Dropdowns for X and Y axis selection
    columns = data.columns.tolist()
    x_column = st.selectbox("Select X-axis column", columns)
    y_column = st.selectbox("Select Y-axis column", columns)

    # Dropdown for graph type
    graph_type = st.selectbox("Select Graph Type", ["Line", "Scatter", "Bar", "Pie"])

    # Plot the graph
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
            # Limit to 10 unique categories for readability
            if len(data[x_column].unique()) <= 10:
                plt.pie(
                    data[y_column],
                    labels=data[x_column],
                    autopct='%1.1f%%',
                    startangle=90,
                )
                plt.title(f"{y_column} (Pie Chart)")
            else:
                st.error("Pie chart requires 10 or fewer unique X values.")

        if graph_type != "Pie":
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            st.pyplot(fig)
        else:
            st.pyplot(plt)

    st.write("Tip: Ensure selected columns contain numeric data for better visualization.")
else:
    st.warning("Failed to load the dataset.")
