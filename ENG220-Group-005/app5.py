import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# MUST be the first Streamlit command


#st.title("Group-005")

st.markdown("""
### California Air Pollution Visualization Dashboard

This app provides an interactive interface to explore **California air quality data** from **2019 to 2024**, 
integrated with Streamlit for intuitive exploration.  
Data includes daily readings of various pollutants like **PM2.5**, **CO**, **NO₂**, **Ozone**, and **Lead**, sourced from government monitoring systems.  
You can compare pollutants by year, visualize monthly averages, and explore proportions via bar and pie charts.
""")

# Define file paths (CSV files instead of Excel)
base_path = os.path.dirname(__file__)
file_names = {
    "2024": os.path.join(base_path, "California2024.csv"),
    "2023": os.path.join(base_path, "California2023.csv"),
    "2022": os.path.join(base_path, "California2022.csv"),
    "2021": os.path.join(base_path, "California2021.csv"),
    "2020": os.path.join(base_path, "California2020.csv"),
    "2019": os.path.join(base_path, "California2019.csv"),
}

# Pollutant descriptions
measurement_info = {
    "PM2.5": "Daily Mean PM2.5 Concentration (µg/m³)",
    "CO": "Carbon Monoxide (ppm)",
    "NO2": "Nitrogen Dioxide (ppb)",
    "Ozone": "Ozone (ppm)",
    "Pb": "Lead (µg/m³)",
}

# Function to load data from CSV
def load_data(file_path, pollutant_column):
    try:
        df = pd.read_csv(file_path)

        # Convert date and extract features
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
        df.dropna(subset=['Date'], inplace=True)
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year

        if pollutant_column not in df.columns:
            st.warning(f"'{pollutant_column}' not found in {os.path.basename(file_path)}")
            return pd.DataFrame(), None

        return df, pollutant_column
    except Exception as e:
        st.error(f"Error reading {os.path.basename(file_path)}: {e}")
        return pd.DataFrame(), None

# UI Controls
pollutants = list(measurement_info.keys())
selected_pollutant = st.selectbox("Select Pollutant", pollutants)
st.markdown(f"**Measurement Info:** {measurement_info[selected_pollutant]}")

measurement_options = ["Measurement"]
if selected_pollutant != "Pb":
    measurement_options.append("AQI")
selected_measurement = st.radio("Select Data Type", measurement_options)

selected_years = st.multiselect("Select Years", list(file_names.keys()), default=list(file_names.keys()))

# Load and combine data
dataframes = []
measurement_column_name = "Daily Mean PM2.5 Concentration" if selected_pollutant == "PM2.5" else selected_pollutant

for year in selected_years:
    df, measurement_col = load_data(file_names[year], measurement_column_name)
    if not df.empty:
        dataframes.append(df)

if dataframes:
    all_data = pd.concat(dataframes, ignore_index=True)

    if selected_measurement == "AQI":
        measurement_column_name = "Daily AQI Value"

    if measurement_column_name not in all_data.columns:
        st.error(f"The selected column '{measurement_column_name}' is not available.")
    else:
        grouped_data = all_data.groupby(['Year', 'Month'])[measurement_column_name].mean().reset_index()

        # Line Chart
        st.subheader(f"{selected_pollutant} Monthly Averages (Line Plot)")
        fig, ax = plt.subplots(figsize=(10, 6))
        for year in grouped_data['Year'].unique():
            year_data = grouped_data[grouped_data['Year'] == year]
            ax.plot(year_data['Month'], year_data[measurement_column_name], label=str(year))
        ax.set_title(f"Monthly Avg of {measurement_column_name} for {selected_pollutant}")
        ax.set_xlabel("Month")
        ax.set_ylabel(measurement_column_name)
        ax.legend()
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        st.pyplot(fig)

        if selected_measurement == "Measurement":
            # Bar Chart
            bar_data = all_data.groupby('Year')[measurement_column_name].sum().reset_index()
            st.subheader(f"Total {selected_pollutant} Values by Year (Bar Chart)")
            bar_fig, ax = plt.subplots()
            ax.bar(bar_data['Year'], bar_data[measurement_column_name])
            ax.set_xlabel("Year")
            ax.set_ylabel(f"Total {measurement_column_name}")
            ax.set_title(f"Total {selected_pollutant} by Year")
            st.pyplot(bar_fig)

            # Pie Chart
            st.subheader(f"Proportion of {selected_pollutant} Values by Year (Pie Chart)")
            pie_fig, ax = plt.subplots()
            ax.pie(bar_data[measurement_column_name], labels=bar_data['Year'], autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Proportion of Total {measurement_column_name} by Year")
            st.pyplot(pie_fig)

        st.subheader("Grouped Monthly Average Data")
        st.dataframe(grouped_data)
else:
    st.error("No data loaded. Please check file names or pollutant selection.")
