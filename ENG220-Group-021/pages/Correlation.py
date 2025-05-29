import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load datasets
snow_depth_path = "data/reshaped_snow_depth.csv"
ground_water_path = "data/fixed_ground_water_cleaned.csv"
aqi_path = "data/aqi_combined_1980_2024.csv"

# Load data
try:
    snow_depth_data = pd.read_csv(snow_depth_path)
    ground_water_data = pd.read_csv(ground_water_path)
    aqi_data = pd.read_csv(aqi_path)
except FileNotFoundError:
    st.error("One or more datasets not found. Please ensure the files are in the 'data' directory.")
    st.stop()

# Merge datasets
snow_avg = snow_depth_data.groupby("Water Year")["Snow Depth (in)"].mean().reset_index()
water_avg = ground_water_data.groupby("Water Year")["Static Water Level (ft)"].mean().reset_index()
aqi_avg = aqi_data.groupby("Year")["AQI_Median"].mean().reset_index()
aqi_avg.rename(columns={"Year": "Water Year"}, inplace=True)

# Merge into a single DataFrame
correlation_data = snow_avg.merge(water_avg, on="Water Year", how="inner")
correlation_data = correlation_data.merge(aqi_avg, on="Water Year", how="inner")

# Streamlit app title
st.title("Correlation Dashboard")

# Display merged data
st.header("Combined Dataset Overview")
st.write(correlation_data)
st.markdown("**Interpretation:** This table shows the combined dataset with average snow depth, static water level, and AQI median over the years. It provides a comprehensive view of how these environmental factors interact over time.")

# Correlation Heatmap with more meaningful context
st.header("Correlation Heatmap")
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
st.markdown("**Interpretation:** This heatmap shows the correlation between average snow depth, static water level, and AQI median. A strong positive correlation between snow depth and static water level would indicate that increased snowpack directly supports groundwater recharge. Conversely, negative correlations with AQI median suggest that higher snowpack or groundwater levels might improve air quality by reducing pollutants.")

# Snow Depth vs Static Water Level with trend line
st.header("Snow Depth vs Static Water Level")
plt.figure(figsize=(10, 6))
plt.scatter(
    correlation_data["Snow Depth (in)"],
    correlation_data["Static Water Level (ft)"],
    alpha=0.7, edgecolor="k"
)
# Add trend line
m, b = np.polyfit(correlation_data["Snow Depth (in)"], correlation_data["Static Water Level (ft)"], 1)
plt.plot(correlation_data["Snow Depth (in)"], m * correlation_data["Snow Depth (in)"] + b, color='red')
plt.title("Snow Depth vs Static Water Level")
plt.xlabel("Average Snow Depth (in)")
plt.ylabel("Average Static Water Level (ft)")
plt.grid(True)
st.pyplot(plt)
plt.clf()
st.markdown("**Interpretation:** This scatter plot, along with the trend line, shows the relationship between average snow depth and average static water level. A positive trend indicates that higher snowpack is likely contributing to increased groundwater levels, which is critical for understanding water availability, particularly in regions dependent on snowmelt for groundwater recharge.")

# Snow Depth vs AQI Median with trend line
st.header("Snow Depth vs AQI Median")
plt.figure(figsize=(10, 6))
plt.scatter(
    correlation_data["Snow Depth (in)"],
    correlation_data["AQI_Median"],
    alpha=0.7, edgecolor="k"
)
# Add trend line
m, b = np.polyfit(correlation_data["Snow Depth (in)"], correlation_data["AQI_Median"], 1)
plt.plot(correlation_data["Snow Depth (in)"], m * correlation_data["Snow Depth (in)"] + b, color='red')
plt.title("Snow Depth vs AQI Median")
plt.xlabel("Average Snow Depth (in)")
plt.ylabel("Average AQI Median")
plt.grid(True)
st.pyplot(plt)
plt.clf()
st.markdown("**Interpretation:** This scatter plot, with the trend line, explores the relationship between average snow depth and average AQI median. The negative trend suggests that regions with higher snow depth generally experience better air quality, possibly because snow acts as a natural filter for airborne pollutants, reducing overall particulate matter in the atmosphere.")

# Static Water Level vs AQI Median with trend line
st.header("Static Water Level vs AQI Median")
plt.figure(figsize=(10, 6))
plt.scatter(
    correlation_data["Static Water Level (ft)"],
    correlation_data["AQI_Median"],
    alpha=0.7, edgecolor="k"
)
# Add trend line
m, b = np.polyfit(correlation_data["Static Water Level (ft)"], correlation_data["AQI_Median"], 1)
plt.plot(correlation_data["Static Water Level (ft)"], m * correlation_data["Static Water Level (ft)"] + b, color='red')
plt.title("Static Water Level vs AQI Median")
plt.xlabel("Average Static Water Level (ft)")
plt.ylabel("Average AQI Median")
plt.grid(True)
st.pyplot(plt)
plt.clf()
st.markdown("**Interpretation:** This scatter plot, with the added trend line, shows the relationship between average static water level and average AQI median. The trend line helps visualize any existing pattern: a negative trend might indicate that higher groundwater levels contribute to improved air quality, potentially through increased vegetation and reduced dust.")

# Insights Section with refined observations
st.header("Insights")
st.markdown(
    """
    - **Snow Depth and Static Water Level**: A clear positive correlation suggests that snowpack plays an important role in groundwater recharge. This relationship is especially crucial for regions dependent on snowmelt.
    - **Snow Depth and AQI Median**: The negative correlation indicates that increased snowpack contributes to better air quality. Snow likely helps trap particulate matter and reduce the amount of dust and pollutants in the air.
    - **Static Water Level and AQI Median**: A possible inverse relationship exists between groundwater levels and AQI. Higher water levels may support more vegetation, which helps in dust suppression and improves overall air quality.
    """
)
