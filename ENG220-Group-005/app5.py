# Group 005 - California Air Pollution Dashboard

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Title and description
#st.title("Group-005")

st.markdown("""
### California Air Pollution Visualization Dashboard

This app provides an interactive interface to explore **California air quality data** from **2019 to 2024**, 
integrated with Streamlit for intuitive exploration.  
Data includes daily readings of various pollutants like **CO, NO₂, Ozone, PM2.5, and Lead**, sourced from government monitoring systems.  
You can compare pollutants by year, visualize monthly averages, and explore proportions via bar and pie charts.
""")

# Base directory and file mappings
base_path = os.path.dirname(__file__)
file_names = {
    "2024": os.path.join(base_path, "..", "California2024.xlsx"),
    "2023": os.path.join(base_path, "California2023.xlsx"),
    "2022": os.path.join(base_path, "California2022.xlsx"),
    "2021": os.path.join(base_path, "California2021.xlsx"),
    "2020": os.path.join(base_path, "California2020.xlsx"),
    "2019": os.path.join(base_path, "California2019.xlsx"),
}

# Measurement unit descriptions
measurement_info = {
    "CO": "Measured in parts per million (ppm)",
    "Pb": "Measured in micrograms per cubic meter (µg/m³)",
    "NO2": "Measured in parts per billion (ppb)",
    "Ozone": "Measured in parts per million (ppm)",
    "PM2.5": "Measured in micrograms per cubic meter (µg/m³)",
}

# Function to load Excel sheet
def load_data(file_path, sheet_name):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")
        measurement_col = df.columns[1]
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        return df, measurement_col
    except Exception as e:
        st.error(f"Error loading {sheet_name} from {os.path.basename(file_path)}: {e}")
        return pd.DataFrame(), None

# Selection interface on main page
pollutants = list(measurement_info.keys())
selected_sheet = st.selectbox("Select Pollutant Sheet", pollutants)
st.markdown(f"**Measurement Info:** {measurement_info[selected_sheet]}")

measurement_options = ["Measurement"]
if selected_sheet != "Pb":
    measurement_options.append("AQI")
selected_measurement = st.radio("Select Data Type", measurement_options)

selected_years = st.multiselect("Select Years", list(file_names.keys()), default=list(file_names.keys()))

# Load and combine selected data
dataframes = []
measurement_column_name = None

for year in selected_years:
    df, measurement_col = load_data(file_names[year], selected_sheet)
    if not df.empty:
        dataframes.append(df)
        if measurement_column_name is None:
            measurement_column_name = measurement_col

if dataframes:
    all_data = pd.concat(dataframes, ignore_index=True)

    if selected_measurement == "AQI":
        measurement_column_name = "Daily AQI Value"

    if measurement_column_name not in all_data.columns:
        st.error(f"The selected measurement column '{measurement_column_name}' is not available.")
    else:
        grouped_data = all_data.groupby(['Year', 'Month'])[measurement_column_name].mean().reset_index()

        # Line Chart
        st.subheader(f"{selected_sheet} Monthly Averages (Line Plot)")
        fig, ax = plt.subplots(figsize=(10, 6))
        for year in grouped_data['Year'].unique():
            year_data = grouped_data[grouped_data['Year'] == year]
            ax.plot(year_data['Month'], year_data[measurement_column_name], label=str(year))
        ax.set_title(f"Monthly Average {measurement_column_name} for {selected_sheet}")
        ax.set_xlabel("Month")
        ax.set_ylabel(measurement_column_name)
        ax.legend()
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        st.pyplot(fig)

        # Bar and Pie charts
        if selected_measurement == "Measurement":
            bar_data = all_data.groupby('Year')[measurement_column_name].sum().reset_index()

            st.subheader(f"Total {selected_sheet} Values by Year (Bar Chart)")
            bar_fig, ax = plt.subplots()
            ax.bar(bar_data['Year'], bar_data[measurement_column_name])
            ax.set_xlabel("Year")
            ax.set_ylabel(f"Total {measurement_column_name}")
            ax.set_title(f"Total {selected_sheet} by Year")
            st.pyplot(bar_fig)

            st.subheader(f"Proportion of {selected_sheet} Values by Year (Pie Chart)")
            pie_fig, ax = plt.subplots()
            ax.pie(bar_data[measurement_column_name], labels=bar_data['Year'], autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Proportion of Total {measurement_column_name} by Year")
            st.pyplot(pie_fig)

        st.subheader("Grouped Monthly Average Data")
        st.dataframe(grouped_data)
else:
    st.error("No data loaded. Check file availability or sheet selection.")
