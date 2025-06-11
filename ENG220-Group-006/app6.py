# -*- coding: utf-8 -*-
# Group 006 - Southern US Air Quality Visualization

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
#st.title("Group-006")

st.markdown("""
### Southern United States Air Quality Visualization

This project is intended to visualize the **Air Quality Data** from **four Southern/Southwestern states in the U.S.**, along with **Hawaii**.  
We analyzed data for **four different pollutants**:
- Carbon Dioxide (**CO₂**)
- Nitrogen Dioxide (**NO₂**)
- Ozone
- **PM2.5** (particles less than 2.5µm in diameter)

The project uses **Streamlit** to provide an interactive and easy-to-use interface for data exploration.
""")

# GitHub source link
st.markdown("[View Source on GitHub](https://github.com/CJLawson175/ENG220_Group-6.git)")

# Cached data loader
@st.cache_data
def load_data():
    file_url = 'https://raw.githubusercontent.com/CJLawson175/ENG220-Group-6/main/ENG220_Data_Filtered.csv'
    return pd.read_csv(file_url)

# Load data
data = load_data()

# Ensure required columns exist
if 'Year' in data.columns and 'Month' in data.columns:
    data['Date'] = pd.to_datetime(data[['Year', 'Month']].assign(DAY=1))

    # State selection
    states = sorted(data['State'].unique())
    selected_state = st.selectbox("Select State", states)

    # Filter by state
    state_data = data[data['State'] == selected_state]

    # County selection
    counties = sorted(state_data['County'].unique())
    selected_county = st.selectbox("Select County", counties)

    # Filter by county
    filtered_data = state_data[state_data['County'] == selected_county]

    # Y-axis pollutant selection
    y_column = st.selectbox(
        "Select Pollutant",
        ["CO2 (ppm)", "NO2 (ppb)", "Ozone (ppm)", "PM2.5 (ug/m3)", "Monthly AQI Average"]
    )

    # Graph type selection
    graph_type = st.selectbox("Select Graph Type", ["Line", "Scatter", "Bar"])

    # Plot the graph
    if not filtered_data.empty:
        fig, ax = plt.subplots(figsize=(10, 6))

        if graph_type == "Line":
            ax.plot(filtered_data['Date'], filtered_data[y_column], marker='o')
            ax.set_title(f"{y_column} vs Date (Line Plot) for {selected_county}, {selected_state}")

        elif graph_type == "Scatter":
            ax.scatter(filtered_data['Date'], filtered_data[y_column])
            ax.set_title(f"{y_column} vs Date (Scatter Plot) for {selected_county}, {selected_state}")

        elif graph_type == "Bar":
            ax.bar(filtered_data['Date'], filtered_data[y_column])
            ax.set_title(f"{y_column} vs Date (Bar Chart) for {selected_county}, {selected_state}")

        ax.set_xlabel("Date")
        ax.set_ylabel(y_column)
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning(f"No data available for {selected_county}, {selected_state}.")

    st.info("Tip: Some counties may not have complete records for all pollutants.")
else:
    st.error("The CSV file must contain 'Year' and 'Month' columns.")
