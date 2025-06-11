
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Resolve paths relative to current file location
current_dir = os.path.dirname(__file__)
snow_depth_path = os.path.abspath(os.path.join(current_dir, "..", "data", "reshaped_snow_depth.csv"))
ground_water_path = os.path.abspath(os.path.join(current_dir, "..", "data", "fixed_ground_water_cleaned.csv"))
aqi_path = os.path.abspath(os.path.join(current_dir, "..", "data", "aqi_combined_1980_2024.csv"))

# Load datasets
try:
    snow_depth_data = pd.read_csv(snow_depth_path)
    ground_water_data = pd.read_csv(ground_water_path)
    aqi_data = pd.read_csv(aqi_path)
except FileNotFoundError:
    st.error("One or more datasets not found. Please ensure the files are in the 'data/' directory.")
    st.stop()

# Merge datasets
snow_avg = snow_depth_data.groupby("Water Year")["Snow Depth (in)"].mean().reset_index()
water_avg = ground_water_data.groupby("Water Year")["Static Water Level (ft)"].mean().reset_index()
aqi_avg = aqi_data.groupby("Year")["AQI_Median"].mean().reset_index()
aqi_avg.rename(columns={"Year": "Water Year"}, inplace=True)

correlation_data = snow_avg.merge(water_avg, on="Water Year", how="inner")
correlation_data = correlation_data.merge(aqi_avg, on="Water Year", how="inner")

# Title
st.title("Correlation Dashboard: Snow, Water & Air Quality")

# Combined Dataset Table
st.subheader("Combined Dataset Overview")
st.dataframe(correlation_data)
st.markdown("**Interpretation:** This table integrates snow depth, groundwater level, and air quality index over the years to observe trends and interdependencies.")

# Correlation Heatmap
st.subheader("Correlation Heatmap")
plt.figure(figsize=(10, 6))
corr_matrix = correlation_data.drop(columns="Water Year").corr()
plt.imshow(corr_matrix, cmap="coolwarm", aspect="auto")
plt.colorbar(label="Correlation Coefficient")
plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=45, ha="right")
plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
plt.title("Correlation Between Variables")
for i in range(len(corr_matrix.columns)):
    for j in range(len(corr_matrix.columns)):
        plt.text(j, i, f"{corr_matrix.iloc[i, j]:.2f}", ha="center", va="center", color="black")
st.pyplot(plt)
plt.clf()
st.markdown("**Interpretation:** This heatmap visualizes how snow depth, static water levels, and AQI values relate to one another through correlation coefficients.")

# Snow Depth vs Static Water Level
st.subheader("Snow Depth vs Static Water Level")
plt.figure(figsize=(10, 6))
plt.scatter(correlation_data["Snow Depth (in)"], correlation_data["Static Water Level (ft)"], alpha=0.7, edgecolor='k')
m, b = np.polyfit(correlation_data["Snow Depth (in)"], correlation_data["Static Water Level (ft)"], 1)
plt.plot(correlation_data["Snow Depth (in)"], m * correlation_data["Snow Depth (in)"] + b, color='red')
plt.title("Snow Depth vs Static Water Level")
plt.xlabel("Avg Snow Depth (in)")
plt.ylabel("Avg Static Water Level (ft)")
plt.grid(True)
st.pyplot(plt)
plt.clf()

# Snow Depth vs AQI Median
st.subheader("Snow Depth vs AQI Median")
plt.figure(figsize=(10, 6))
plt.scatter(correlation_data["Snow Depth (in)"], correlation_data["AQI_Median"], alpha=0.7, edgecolor='k')
m, b = np.polyfit(correlation_data["Snow Depth (in)"], correlation_data["AQI_Median"], 1)
plt.plot(correlation_data["Snow Depth (in)"], m * correlation_data["Snow Depth (in)"] + b, color='red')
plt.title("Snow Depth vs AQI Median")
plt.xlabel("Avg Snow Depth (in)")
plt.ylabel("Avg AQI Median")
plt.grid(True)
st.pyplot(plt)
plt.clf()

# Static Water Level vs AQI Median
st.subheader("Static Water Level vs AQI Median")
plt.figure(figsize=(10, 6))
plt.scatter(correlation_data["Static Water Level (ft)"], correlation_data["AQI_Median"], alpha=0.7, edgecolor='k')
m, b = np.polyfit(correlation_data["Static Water Level (ft)"], correlation_data["AQI_Median"], 1)
plt.plot(correlation_data["Static Water Level (ft)"], m * correlation_data["Static Water Level (ft)"] + b, color='red')
plt.title("Static Water Level vs AQI Median")
plt.xlabel("Avg Static Water Level (ft)")
plt.ylabel("Avg AQI Median")
plt.grid(True)
st.pyplot(plt)
plt.clf()

# Summary
st.subheader("Insights")
st.markdown("""
- **Snow Depth and Static Water Level**: Strong positive correlation suggests snowpack significantly contributes to groundwater recharge.
- **Snow Depth and AQI**: Negative correlation implies snow helps improve air quality by trapping pollutants.
- **Water Level and AQI**: Inverse relationship hints that higher groundwater may support vegetation, improving air quality indirectly.
""")

st.markdown("Use the navigation to return to the homepage or explore other insights in Project 21.")
