
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Set current directory for compatibility with unified dashboard
current_dir = os.path.dirname(__file__)
snow_depth_path = os.path.abspath(os.path.join(current_dir, "..", "data", "reshaped_snow_depth.csv"))
ground_water_path = os.path.abspath(os.path.join(current_dir, "..", "data", "fixed_ground_water_cleaned.csv"))

# Load the datasets
try:
    snow_depth_data = pd.read_csv(snow_depth_path)
    ground_water_data = pd.read_csv(ground_water_path)
except FileNotFoundError:
    st.error("Dataset not found. Please ensure the files exist in the 'data/' directory.")
    st.stop()

# Ensure required columns exist
snow_columns = snow_depth_data.columns
ground_columns = ground_water_data.columns

# Sidebar options
st.sidebar.header("Dashboard Options")

# Year range selection for snow depth data
if "Water Year" in snow_columns:
    years = sorted(snow_depth_data["Water Year"].unique())
    selected_years = st.sidebar.slider(
        "Select Year Range",
        int(min(years)),
        int(max(years)),
        (int(min(years)), int(max(years)))
    )
else:
    st.error("The 'Water Year' column is missing in the snow depth dataset.")
    st.stop()

# Site selection for snow depth analysis
if "Site" in snow_columns:
    selected_site = st.sidebar.selectbox("Select Site", snow_depth_data["Site"].unique())
else:
    st.warning("The 'Site' column is missing in the dataset.")
    selected_site = None

# Filter snow depth data based on selections
filtered_snow_data = snow_depth_data[(snow_depth_data["Water Year"] >= selected_years[0]) & (snow_depth_data["Water Year"] <= selected_years[1])]
if selected_site:
    filtered_snow_data = filtered_snow_data[filtered_snow_data["Site"] == selected_site]

# Display header
st.title("\U0001F30A Water Resource Dashboard")

# 1. Yearly Snow Depth Trends
st.subheader("Yearly Snow Depth Trends")
if not filtered_snow_data.empty:
    yearly_trends = filtered_snow_data.groupby("Water Year")["Snow Depth (in)"].mean()
    plt.figure(figsize=(10, 6))
    plt.scatter(yearly_trends.index, yearly_trends, color='blue', alpha=0.7, edgecolor='k')
    m, b = np.polyfit(yearly_trends.index, yearly_trends, 1)
    plt.plot(yearly_trends.index, m * yearly_trends.index + b, color='red')
    plt.title(f"Yearly Snow Depth Trends for {selected_site}")
    plt.xlabel("Year")
    plt.ylabel("Average Snow Depth (in)")
    plt.grid(True)
    st.pyplot(plt)
    plt.clf()
    st.markdown("**Interpretation:** This graph shows the average snow depth over the years for the selected site, along with a trend line.")
else:
    st.warning("No data available for the selected site and year range.")

# 2. Static Water Level Trends
st.subheader("Static Water Level Trends")
if "Water Year" in ground_columns:
    filtered_ground_data = ground_water_data[(ground_water_data["Water Year"] >= selected_years[0]) & (ground_water_data["Water Year"] <= selected_years[1])]
    avg_water_level = filtered_ground_data.groupby("Water Year")["Static Water Level (ft)"].mean()
    if not avg_water_level.empty:
        plt.figure(figsize=(10, 6))
        plt.scatter(avg_water_level.index, avg_water_level, color='green', alpha=0.7, edgecolor='k')
        m, b = np.polyfit(avg_water_level.index, avg_water_level, 1)
        plt.plot(avg_water_level.index, m * avg_water_level.index + b, color='red')
        plt.title("Static Water Level Trends")
        plt.xlabel("Year")
        plt.ylabel("Average Static Water Level (ft)")
        plt.grid(True)
        st.pyplot(plt)
        plt.clf()
        st.markdown("**Interpretation:** This graph shows the average static water level over the years with a trend line.")
    else:
        st.warning("No valid data available for Static Water Level Trends.")
else:
    st.error("The 'Water Year' column is missing in the ground water dataset.")
    st.stop()

# 3. Snow Depth vs Static Water Level Correlation
st.subheader("Snow Depth vs Static Water Level Correlation")
combined_data = filtered_snow_data.groupby("Water Year")["Snow Depth (in)"].mean().reset_index()
if "Water Year" in ground_columns:
    combined_data = combined_data.merge(
        filtered_ground_data.groupby("Water Year")["Static Water Level (ft)"].mean().reset_index(),
        on="Water Year",
        how="inner"
    )
    if not combined_data.empty:
        plt.figure(figsize=(10, 6))
        plt.scatter(
            combined_data["Snow Depth (in)"],
            combined_data["Static Water Level (ft)"],
            alpha=0.7, edgecolor='k'
        )
        m, b = np.polyfit(combined_data["Snow Depth (in)"], combined_data["Static Water Level (ft)"], 1)
        plt.plot(combined_data["Snow Depth (in)"], m * combined_data["Snow Depth (in)"] + b, color='red')
        plt.title("Correlation Between Snow Depth and Static Water Level")
        plt.xlabel("Average Snow Depth (in)")
        plt.ylabel("Average Static Water Level (ft)")
        plt.grid(True)
        st.pyplot(plt)
        plt.clf()
        st.markdown("**Interpretation:** This scatter plot shows the correlation between snow depth and static water level.")
    else:
        st.warning("No valid data available for correlation analysis.")
else:
    st.warning("Data for correlation is not available.")

# 4. Top Sites with Greatest Resource Decline
st.subheader("Top Sites with Greatest Resource Decline")
snow_decline = snow_depth_data.groupby("Site")["Snow Depth (in)"].agg(["first", "last"])
snow_decline["Decline"] = snow_decline["first"] - snow_decline["last"]
top_decline_sites = snow_decline.nlargest(10, "Decline")["Decline"].reset_index()
plt.figure(figsize=(10, 6))
plt.barh(top_decline_sites["Site"], top_decline_sites["Decline"], color="skyblue")
plt.title("Top Sites with Greatest Snow Depth Decline")
plt.xlabel("Decline in Snow Depth (in)")
plt.ylabel("Site")
plt.grid(True, axis="x")
st.pyplot(plt)
plt.clf()
st.markdown("**Interpretation:** This chart highlights sites with the greatest snow depth decline over time.")

# 5. Overall Trends Across All Sites and Years
st.subheader("Overall Trends Across All Sites and Years")
overall_snow_depth = snow_depth_data.groupby("Water Year")["Snow Depth (in)"].mean().reset_index()
overall_water_level = ground_water_data.groupby("Water Year")["Static Water Level (ft)"].mean().reset_index()
combined_overall = overall_snow_depth.merge(overall_water_level, on="Water Year", how="inner")

if not combined_overall.empty:
    plt.figure(figsize=(10, 6))
    plt.plot(combined_overall["Water Year"], combined_overall["Snow Depth (in)"], marker='o', color='blue', label='Avg Snow Depth')
    plt.plot(combined_overall["Water Year"], combined_overall["Static Water Level (ft)"], marker='o', color='green', label='Avg Static Water Level')
    m_snow, b_snow = np.polyfit(combined_overall["Water Year"], combined_overall["Snow Depth (in)"], 1)
    plt.plot(combined_overall["Water Year"], m_snow * combined_overall["Water Year"] + b_snow, color='blue', linestyle='--')
    m_water, b_water = np.polyfit(combined_overall["Water Year"], combined_overall["Static Water Level (ft)"], 1)
    plt.plot(combined_overall["Water Year"], m_water * combined_overall["Water Year"] + b_water, color='green', linestyle='--')
    plt.title("Overall Trends Across All Sites and Years")
    plt.xlabel("Year")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    plt.clf()
    st.markdown("**Interpretation:** This graph provides a combined view of trends in snow and water levels across all years.")
else:
    st.warning("No valid data available for overall trends.")

st.markdown("Return to homepage using the navigation menu.")
