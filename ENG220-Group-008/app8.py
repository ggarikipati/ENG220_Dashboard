# -*- coding: utf-8 -*-
# Group 008 - Environmental Measurements Dashboard

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Title
st.title("Group-008")

st.markdown("""
### Environmental Measurements Visualization Dashboard

This project is a **Streamlit-based web application** designed to visualize environmental measurement data collected from the **EPA (Environmental Protection Agency)**.  
It provides interactive visualizations for **monthly measurements across various materials**, counties, and states.

Users can:
- Explore data using **bar and line graphs**
- Filter by **state, county, and pollutant/material**
- Understand **measurement trends and yearly averages** across different locations

---
""")

# Load CSV file relative to app location
@st.cache_data
def load_data():
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "filtered_data_updated.csv")
    return pd.read_csv(csv_path)

# Load the dataset
filtered_data_df = load_data()

# Cascading dropdowns
state = st.selectbox("Select State", filtered_data_df['State'].unique())
county_options = filtered_data_df[filtered_data_df['State'] == state]['County'].unique()
county = st.selectbox("Select County", county_options)
material_options = filtered_data_df[
    (filtered_data_df['State'] == state) & (filtered_data_df['County'] == county)
]['Material'].unique()
material = st.selectbox("Select Material", material_options)

# Graph type
graph_type = st.radio("Select Graph Type", ['Bar Graph', 'Line Graph'])

# Filter dataset
filtered_data = filtered_data_df[
    (filtered_data_df['State'] == state) &
    (filtered_data_df['County'] == county) &
    (filtered_data_df['Material'] == material)
]

if filtered_data.empty:
    st.warning("No data available for the selected options.")
else:
    unit = 'µg/m³' if material == 'PM2.5' else 'ppm' if material in ['CO', 'Ozone'] else 'ppb'

    if graph_type == 'Bar Graph':
        st.subheader(f"Bar Graph on {material} in {county}, {state}")
        monthly_data = filtered_data.pivot(index='Year', columns='Month', values='Monthly Measurements')
        yearly_avg = filtered_data['Yearly Measurement Average'].mean()

        fig, ax = plt.subplots(figsize=(12, 6))
        monthly_data.plot(kind='bar', ax=ax)
        ax.axhline(y=yearly_avg, color='red', linestyle='--', label='Yearly Average')
        ax.set_xlabel('Year')
        ax.set_ylabel(f"Monthly {material} ({unit})")
        ax.set_title(f"{material} Levels in {county}, {state} by Month")
        ax.legend()
        st.pyplot(fig)

    else:
        st.subheader(f"Line Graph on {material} in {county}, {state}")
        line_data = filtered_data.groupby(['Year', 'Month'])['Monthly Measurements'].mean().reset_index()
        line_data['Date'] = pd.to_datetime(line_data[['Year', 'Month']].assign(DAY=1))

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(line_data['Date'], line_data['Monthly Measurements'], label=f"{material} Measurements", marker='o')
        ax.set_xlabel('Date')
        ax.set_ylabel(f"Monthly {material} ({unit})")
        ax.set_title(f"{material} Trends in {county}, {state} Over Time")
        ax.legend()
        st.pyplot(fig)

    st.info("Tip: Use the graph type selector to compare yearly trends or monthly distributions.")
