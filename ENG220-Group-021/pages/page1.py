
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# File path for the dataset (for unified dashboard)
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "..", "data", "aqi_combined_1980_2024.csv")
file_path = os.path.abspath(file_path)

# Load the dataset
try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("Dataset not found. Please ensure the file is in the correct path: 'data/aqi_combined_1980_2024.csv'")
    st.stop()

# Ensure required columns exist
available_columns = data.columns

# Sidebar options
st.sidebar.header("Dashboard Options")

# Year range selection
years = sorted(data["Year"].unique()) if "Year" in available_columns else []
if not years:
    st.error("The 'Year' column is missing in the dataset.")
    st.stop()

selected_years = st.sidebar.slider(
    "Select Year Range",
    int(min(years)),
    int(max(years)),
    (int(min(years)), int(max(years)))
)

# CBSA selection
if "CBSA" in available_columns:
    selected_cbsa = st.sidebar.selectbox("Select CBSA", data["CBSA"].unique())
else:
    st.warning("The 'CBSA' column is missing in the dataset.")
    selected_cbsa = None

# Filter data based on selections
filtered_data = data[(data["Year"] >= selected_years[0]) & (data["Year"] <= selected_years[1])]
if selected_cbsa:
    filtered_data = filtered_data[filtered_data["CBSA"] == selected_cbsa]

# Display header
st.title("Air Quality Viewer Dashboard")

# Section 1: Overall AQI Trends
st.subheader("Overall Air Quality Trends (1980–2024)")
if "AQI_Median" in available_columns:
    overall_aqi = data.groupby("Year")["AQI_Median"].mean()
    if not overall_aqi.empty:
        plt.figure(figsize=(10, 6))
        overall_aqi.plot(marker='o', color='blue')
        plt.title("Overall AQI Trends")
        plt.xlabel("Year")
        plt.ylabel("Average AQI Median")
        plt.grid(True)
        st.pyplot(plt)
        plt.clf()
        st.markdown("**Interpretation:** This trend shows changes in air quality over time. A downward slope suggests improvements in air quality.")
    else:
        st.warning("No data available for AQI trends.")
else:
    st.warning("'AQI_Median' column not found.")

# Section 2: AQI Days by Category
categories = ["Good", "Moderate", "Unhealthy_for_Sensitive_Groups", "Unhealthy", "Very_Unhealthy", "Hazardous"]
if all(col in available_columns for col in categories):
    st.subheader("AQI Days by Category")
    category_sums = filtered_data[categories].sum()
    category_sums = pd.to_numeric(category_sums, errors="coerce").fillna(0)
    if not category_sums.empty:
        plt.figure(figsize=(8, 6))
        plt.bar(category_sums.index, category_sums.values, color='skyblue')
        plt.title("AQI Days by Category")
        plt.xlabel("Category")
        plt.ylabel("Number of Days")
        plt.grid(axis="y")
        for i, val in enumerate(category_sums.values):
            plt.text(i, val + 1, str(int(val)), ha='center')
        st.pyplot(plt)
        plt.clf()
        st.markdown("**Interpretation:** Categorization of AQI helps understand the frequency of clean vs unhealthy air days.")
    else:
        st.warning("No category data found.")
else:
    st.warning("One or more AQI category columns are missing.")

# Section 3: Pollutant Days by Year
pollutant_columns = ["#_Days_CO", "#_Days_NO2", "#_Days_O3", "#_Days_PM2.5", "#_Days_PM10"]
if all(col in available_columns for col in pollutant_columns):
    st.subheader("Pollutant Days by Year")
    for col in pollutant_columns:
        filtered_data[col] = pd.to_numeric(filtered_data[col], errors="coerce").fillna(0)
    yearly_pollutants = filtered_data.groupby("Year")[pollutant_columns].sum()
    if not yearly_pollutants.empty and yearly_pollutants.sum().sum() > 0:
        yearly_pollutants.plot(kind="bar", stacked=True, figsize=(10, 6), color=plt.cm.tab10.colors)
        plt.title("Pollutant Days by Year")
        plt.xlabel("Year")
        plt.ylabel("Number of Days")
        plt.grid(axis="y")
        st.pyplot(plt)
        plt.clf()
        st.markdown("**Interpretation:** Tracks how often each pollutant exceeded safe levels over the years.")
    else:
        st.warning("No pollutant trend data available.")
else:
    st.warning("Missing pollutant day columns.")

# Section 4: AQI Statistics
if all(col in available_columns for col in ["AQI_Maximum", "AQI_90th_Percentile", "AQI_Median"]):
    st.subheader("AQI Statistics Over Time")
    aqi_stats = filtered_data.groupby("Year")[["AQI_Maximum", "AQI_90th_Percentile", "AQI_Median"]].mean()
    aqi_stats.plot(figsize=(10, 6), marker='o')
    plt.title("AQI Statistics")
    plt.xlabel("Year")
    plt.ylabel("AQI Value")
    plt.legend(title="Statistic")
    plt.grid(True)
    st.pyplot(plt)
    plt.clf()
    st.markdown("**Interpretation:** Maximum and percentile AQI values reveal peaks and consistent exposure levels.")
else:
    st.warning("Missing AQI statistics columns.")

# Section 5: Summary Table
st.subheader("Filtered Dataset Summary")
st.dataframe(filtered_data)
st.markdown("**Interpretation:** The table displays detailed metrics for the selected CBSA and year range.")
