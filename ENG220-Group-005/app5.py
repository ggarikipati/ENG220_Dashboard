import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ✅ Must be first
#st.set_page_config(page_title="Group-005", layout="wide")

# Title
#st.title("Group-005")

# Description
st.markdown("""
### California Air Pollution Visualization Dashboard

This app provides an interactive interface to explore **California air quality data** from **2019 to 2024**, 
using official monitoring data.  
Visualize trends by **year**, compare **monthly averages**, and explore **AQI vs raw measurements**.

""")

# Base path and file references
base_path = os.path.dirname(__file__)
file_names = {
    "2024": os.path.join(base_path, "California2024.xlsx"),
    "2023": os.path.join(base_path, "California2023.xlsx"),
    "2022": os.path.join(base_path, "California2022.xlsx"),
    "2021": os.path.join(base_path, "California2021.xlsx"),
    "2020": os.path.join(base_path, "California2020.xlsx"),
    "2019": os.path.join(base_path, "California2019.xlsx"),
}

# Pollutants and fallback columns (some files use different column headers)
pollutant_columns = {
    "PM2.5": ["Daily Mean PM2.5 Concentration", "Daily Max 1-hour NO2 Concentration"],
    "NO2": ["Daily Max 1-hour NO2 Concentration"]
}
aqi_column = "Daily AQI Value"

# Load data and detect which column to use
def load_data(file_path, fallback_columns):
    try:
        df = pd.read_excel(file_path)

        # Determine available measurement column
        for col in fallback_columns:
            if col in df.columns:
                measurement_col = col
                break
        else:
            st.warning(f"No valid column found in {os.path.basename(file_path)}.")
            return pd.DataFrame(), None

        # Parse and prepare
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        return df, measurement_col

    except Exception as e:
        st.error(f"Error loading {os.path.basename(file_path)}: {e}")
        return pd.DataFrame(), None

# UI widgets
selected_pollutant = st.selectbox("Select Pollutant", list(pollutant_columns.keys()))
measurement_type = st.radio("Select Data Type", ["Measurement", "AQI"])
selected_years = st.multiselect("Select Years", list(file_names.keys()), default=list(file_names.keys()))

# Load and combine data
dataframes = []
measurement_col = None

for year in selected_years:
    df, detected_col = load_data(file_names[year], pollutant_columns[selected_pollutant])
    if not df.empty:
        if measurement_type == "AQI":
            if aqi_column in df.columns:
                df[aqi_column] = pd.to_numeric(df[aqi_column], errors='coerce')
                measurement_col = aqi_column
            else:
                st.warning(f"{aqi_column} not found in {year} file.")
                continue
        else:
            df[detected_col] = pd.to_numeric(df[detected_col], errors='coerce')
            measurement_col = detected_col

        dataframes.append(df)

# Display
if dataframes and measurement_col:
    all_data = pd.concat(dataframes, ignore_index=True)

    grouped = all_data.groupby(['Year', 'Month'])[measurement_col].mean().reset_index()

    # 📈 Line Chart
    st.subheader(f"{selected_pollutant} Monthly Averages (Line Plot)")
    fig, ax = plt.subplots(figsize=(10, 6))
    for yr in grouped['Year'].unique():
        ax.plot(grouped[grouped['Year'] == yr]['Month'],
                grouped[grouped['Year'] == yr][measurement_col], label=str(yr))
    ax.set_title(f"Monthly Average of {measurement_col}")
    ax.set_xlabel("Month")
    ax.set_ylabel(measurement_col)
    ax.legend()
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    st.pyplot(fig)

    # 📊 Bar + Pie Charts (only for measurement)
    if measurement_type == "Measurement":
        bar_data = all_data.groupby('Year')[measurement_col].sum().reset_index()

        st.subheader(f"Total {selected_pollutant} by Year (Bar Chart)")
        bar_fig, ax = plt.subplots()
        ax.bar(bar_data['Year'], bar_data[measurement_col])
        ax.set_title(f"{selected_pollutant} Total by Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total")
        st.pyplot(bar_fig)

        st.subheader(f"Proportion by Year (Pie Chart)")
        pie_fig, ax = plt.subplots()
        ax.pie(bar_data[measurement_col], labels=bar_data['Year'], autopct='%1.1f%%', startangle=90)
        st.pyplot(pie_fig)

    # 📋 Table
    st.subheader("Grouped Monthly Average Data")
    st.dataframe(grouped)
else:
    st.error("No data loaded. Please check file format, column names, or selections.")
