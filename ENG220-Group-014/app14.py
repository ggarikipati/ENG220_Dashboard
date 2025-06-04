import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set current directory and file path
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'CleanedMHData(Sheet1) (1).csv')

# Title
st.title("Group-014")

# Project description
st.markdown("""
### Mental Health Distress Trends by State

This project visualizes mental health trends across the **United States**, with a particular focus on **New Mexico**.  
It highlights the percentage of survey respondents reporting **frequent mental distress** across the years **2015, 2018, and 2024**, with more detailed data available for New Mexico.  
Users can explore the trends using **Line Graphs**, **Scatter Plots**, **Bar Charts**, or **Pie Charts**, selecting individual states to observe changes over time.
""")

# Load and clean data
try:
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip().str.lower()  # Clean column names
except FileNotFoundError:
    st.error("CSV file not found. Please ensure the file is correctly placed.")
    data = None

if data is not None:
    st.write("### Data Preview")
    st.dataframe(data)

    # Select State
    if 'state' in data.columns:
        state = st.selectbox("Select State", data['state'].unique())

        # Filter state-specific data
        state_data = data[data['state'] == state]

        if state_data.empty:
            st.warning("No data available for the selected state.")
        else:
            x_column = 'total number of survey respondents'
            y_column = 'percentage with mental distress'

            if x_column not in state_data.columns or y_column not in state_data.columns:
                st.error("Required columns not found in the dataset.")
            else:
                years = ", ".join(sorted(state_data['year'].astype(str).unique()))
                chart_title = f"{state} for Years: {years}"

                # Select graph type
                graph_type = st.selectbox("Select Graph Type", ["Line", "Scatter", "Bar", "Pie"])

                # Plot graph
                if st.button("Plot Graph"):
                    fig, ax = plt.subplots()

                    if graph_type == "Line":
                        for year in sorted(state_data['year'].unique()):
                            year_data = state_data[state_data['year'] == year]
                            ax.plot(year_data[x_column], year_data[y_column], label=f"Year {year}", marker='o')

                    elif graph_type == "Scatter":
                        for year in sorted(state_data['year'].unique()):
                            year_data = state_data[state_data['year'] == year]
                            ax.scatter(year_data[x_column], year_data[y_column], label=f"Year {year}")

                    elif graph_type == "Bar":
                        for year in sorted(state_data['year'].unique()):
                            year_data = state_data[state_data['year'] == year]
                            ax.bar(year_data[x_column], year_data[y_column], label=f"Year {year}")

                    elif graph_type == "Pie":
                        # Convert y_column to numeric
                        state_data[y_column] = state_data[y_column].astype(str).str.replace('%', '')
                        state_data[y_column] = pd.to_numeric(state_data[y_column], errors='coerce')

                        pie_data = state_data.groupby('year')[y_column].mean()

                        if pie_data.isnull().all():
                            st.error("No valid numeric data available for pie chart.")
                        else:
                            ax.pie(
                                pie_data,
                                labels=pie_data.index,
                                autopct='%1.1f%%',
                                startangle=90
                            )
                            ax.set_title(chart_title)

                    if graph_type != "Pie":
                        ax.set_title(chart_title)
                        ax.set_xlabel("Total Number of Survey Respondents")
                        ax.set_ylabel("Percentage With Mental Distress")
                        ax.legend(title="Year")
                        st.pyplot(fig)
                    else:
                        st.pyplot(fig)

else:
    st.warning("Failed to load the dataset.")
