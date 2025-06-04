# -*- coding: utf-8 -*-
# Group 003 - McClure Reservoir Water Level Dashboard

import streamlit as st
import pandas as pd
import os

# Title
st.title("Group-003")

st.markdown("""
### McClure Water Reservoir Level with Moving Average

This interactive data dashboard visualizes the water levels of the **McClure Water Reservoir** using **USGS data** collected over the past **17 years**.  
Users can explore both the raw reservoir level data and an overlaid **moving average** to better observe long-term trends, particularly the gradual decline in water levels.
""")

try:
    # Load CSV file relative to this script
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "extracted_data.csv")
    df = pd.read_csv(csv_path)

    st.subheader("Reservoir Level Data")
    st.dataframe(df)

    # Basic bar chart
    st.subheader("Water Level Over Time")
    st.bar_chart(df[['Time (Days)', 'Basin Water Level (Acre ft)']].set_index('Time (Days)'))

    # Option to enable moving average
    if st.checkbox('Show Moving Average'):
        moving_avg_column = 'Basin Water Level (Acre ft)'
        window_size = 1000

        df['Moving Average'] = df[moving_avg_column].rolling(window_size).mean()

        st.subheader(f"Moving Average (Window: {window_size})")
        st.line_chart(df[['Time (Days)', 'Moving Average']].set_index('Time (Days)'))

    st.info("Use the checkbox above to visualize long-term water level trends.")

except FileNotFoundError:
    st.error("The file 'extracted_data.csv' was not found. Please ensure it is in the same folder as this script.")
