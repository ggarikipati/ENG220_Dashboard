# Group 005 - California Air Pollution Dashboard (CSV Version)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Title and description
st.markdown("""
### California Air Pollution Visualization Dashboard

This app provides an interactive interface to explore **California air quality data** from **2019 to 2024**, 
integrated with Streamlit for intuitive exploration.  
Data includes daily readings of various pollutants like **CO, NO₂, Ozone, PM2.5, and Lead**, sourced from government monitoring systems.  
You can compare pollutants by year, visualize monthly averages, and explore proportions via bar and pie charts.
""")

# File paths to CSVs
base_path = os.path.dirname(__file__)
file_names = {
    "2024": os.path.join(base_path, "California2024.csv"),
    "2023": os.path.join(base_path, "California2023.csv"),
    "2022": os.path.join(base_path, "California2022.csv"),
    "2021": os.path.join(base_path, "California2021.csv"),
    "2020": os.path.join(base_path, "California2020.csv"),
    "2019": os.path.join(base_path, "California2019.csv"),
}

# Pollutant metadata
measurement_info = {
    "CO": "Measured in parts per million (ppm)",
    "Pb": "Measured in µg/m³",
    "NO2": "Measured in parts per billion (ppb)",
    "Ozone": "Measured in ppm",
    "PM2.5": "Measured in µg/m³",
}

# Load CSV file for a given pollutant
def load_data(file_path, pollutant_name):
    try:
        df = pd.read_csv(file_path)
        if pollutant_name not in df.columns:
            st.error(f"'{pollutant_name}' not found in {os.path.basename(file_path)}")
            return pd.DataFrame(), None
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        return df, pollutant_name
    except Exception as e:
        st.error(f"Error loading {pollutant_name} from {os.path.basename(file_path)}: {e}")
        return pd.DataFrame(), None

# Sidebar controls
pollutants = list(measurement_info.keys())
selected_pollutant = st.sidebar.selectbox("Select Pollutant", pollutants)
st.sidebar.write(f"**{measurement_info[selected_pollutant]}**")

measurement_options = {"Measurement": selected_pollutant}
if selected_pollutant != "Pb":
    measurement_options["AQI"] = "Daily AQI Value"
selected_measurement = st.sidebar.radio("Select Data Type", list(measurement_options.keys()))

selected_years = st.sidebar.multiselect("Select Years", list(file_names.keys()), default=list(file_names.keys()))

# Load selected data
dataframes = []
measurement_column = None

for year in selected_years:
    df, col = load_data(file_names[year], selected_pollutant)
    if not df.empty:
        dataframes.append(df)
        if measurement_column is None:
            measurement_column = col

if dataframes:
    all_data = pd.concat(dataframes, ignore_index=True)

    if selected_measurement == "AQI":
        measurement_column = "Daily AQI Value"

    if measurement_column not in all_data.columns:
        st.error(f"'{measurement_column}' not available in the data.")
    else:
        grouped = all_data.groupby(['Year', 'Month'])[measurement_column].mean().reset_index()

        # Line chart
        st.subheader(f"{selected_pollutant} Monthly Averages (Line Plot)")
        fig, ax = plt.subplots(figsize=(10, 6))
        for year in grouped['Year'].unique():
            year_data = grouped[grouped['Year'] == year]
            ax.plot(year_data['Month'], year_data[measurement_column], label=str(year))
        ax.set_title(f"Monthly Average of {measurement_column}")
        ax.set_xlabel("Month")
        ax.set_ylabel(measurement_column)
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax.legend()
        st.pyplot(fig)

        if selected_measurement == "Measurement":
            bar_data = all_data.groupby('Year')[measurement_column].sum().reset_index()

            st.subheader(f"Total {selected_pollutant} by Year (Bar Chart)")
            bar_fig, ax = plt.subplots()
            ax.bar(bar_data['Year'], bar_data[measurement_column])
            ax.set_xlabel("Year")
            ax.set_ylabel(measurement_column)
            st.pyplot(bar_fig)

            st.subheader(f"Proportions by Year (Pie Chart)")
            pie_fig, ax = plt.subplots()
            ax.pie(bar_data[measurement_column], labels=bar_data['Year'], autopct='%1.1f%%')
            st.pyplot(pie_fig)

        st.subheader("Grouped Monthly Averages")
        st.dataframe(grouped)
else:
    st.error("No data loaded. Please check file names or pollutant selection.")
