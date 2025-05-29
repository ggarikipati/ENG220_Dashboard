import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# File path for the dataset
file_path = "data/aqi_combined_1980_2024.csv"

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
st.title("🌫️ Air Quality Viewer Dashboard")

# 1. Overall Air Quality Trends (1980-2024)
st.subheader("Overall Air Quality Trends (1980-2024)")
if "AQI_Median" in available_columns:
    overall_aqi = data.groupby("Year")["AQI_Median"].mean()
    if not overall_aqi.empty:
        plt.figure(figsize=(10, 6))
        overall_aqi.plot(marker='o', color='blue')
        plt.title("Overall Air Quality Trends")
        plt.xlabel("Year")
        plt.ylabel("Average AQI Median")
        plt.grid(True)
        st.pyplot(plt)
        plt.clf()
        st.markdown("**Interpretation:** This graph displays the overall trend in Air Quality Index (AQI) median from 1980 to 2024. A decreasing trend may indicate an improvement in air quality over the years, while an increasing trend could suggest worsening conditions. This is crucial for assessing long-term air quality management efforts.")
    else:
        st.warning("No valid data available for Overall Air Quality Trends.")
else:
    st.warning("The 'AQI_Median' column is missing in the dataset.")

# 2. AQI Days by Category
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
            plt.text(i, val + max(category_sums.values) * 0.01, f"{int(val)}", ha='center', va='bottom')
        st.pyplot(plt)
        plt.clf()
        st.markdown("**Interpretation:** This bar chart shows the distribution of AQI days across different categories. A higher number of 'Good' days indicates better air quality, whereas a higher count of 'Unhealthy' or 'Hazardous' days indicates poorer air quality. This helps in understanding the air quality distribution for the selected CBSA and year range.")
    else:
        st.warning("No valid data available for AQI Days by Category.")
else:
    st.warning("Some or all AQI categories are missing in the dataset.")

# 3. Pollutant Days by Year
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
        plt.legend(title="Pollutant")
        plt.grid(axis="y")
        st.pyplot(plt)
        plt.clf()
        st.markdown("**Interpretation:** This stacked bar chart shows the number of days each pollutant was above a certain threshold, by year. It highlights which pollutants are more prevalent over time, helping to identify specific pollutants that contribute significantly to poor air quality in the selected area.")
    else:
        st.warning("No valid data available for Pollutant Days by Year.")
else:
    st.warning("Some or all pollutant columns are missing in the dataset.")

# 4. AQI Statistics
if all(col in available_columns for col in ["AQI_Maximum", "AQI_90th_Percentile", "AQI_Median"]):
    st.subheader("AQI Statistics")
    aqi_stats = filtered_data.groupby("Year")[["AQI_Maximum", "AQI_90th_Percentile", "AQI_Median"]].mean()
    aqi_stats.plot(figsize=(10, 6), marker='o')
    plt.title("AQI Statistics Over Time")
    plt.xlabel("Year")
    plt.ylabel("AQI Value")
    plt.legend(title="Statistic")
    plt.grid(True)
    st.pyplot(plt)
    plt.clf()
    st.markdown("**Interpretation:** This line plot shows key AQI statistics over the years, including maximum values, the 90th percentile, and median. This provides insight into the distribution and severity of air quality issues, indicating whether extreme air quality events are becoming more or less frequent over time.")
else:
    st.warning("Some or all AQI statistic columns are missing in the dataset.")

# 5. CBSA Summary Table
st.subheader("CBSA Summary Table")
st.write(filtered_data)
st.markdown("**Interpretation:** This table provides a detailed summary of the filtered data for the selected CBSA and year range, including all relevant AQI metrics and pollutant information. It allows for in-depth analysis and review of the air quality metrics.")

# Back to Home
st.markdown(
    "<a href='../HomePage.py' style='font-size: 1.2em;'>⬅️ Back to Home</a>",
    unsafe_allow_html=True
)

