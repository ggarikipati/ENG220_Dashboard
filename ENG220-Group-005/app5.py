# Group 005 - California Air Pollution Dashboard

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Description (title is set from dashboard)
st.markdown("""
### California Air Pollution Visualization Dashboard

This app provides an interactive interface to explore **California air quality data** from **2019 to 2024**, 
integrated with Streamlit for intuitive exploration.  
Data includes daily readings of various pollutants like **CO, NO₂, Ozone, PM2.5, and Lead**, sourced from government monitoring systems.  
You can compare pollutants by year, visualize monthly averages, and explore proportions via bar and pie charts.
""")

# Define file paths using current directory
base_path = os.path.dirname(__file__)
file_names = {
    "2024": os.path.join(base_path, "California2024.csv"),
    "2023": os.path.join(base_path, "California2023.csv"),
    "2022": os.path.join(base_path, "California2022.csv"),
    "2021": os.path.join(base_path, "California2021.csv"),
    "2020": os.path.join(base_path, "California2020.csv"),
    "2019": os.path.join(base_path, "California2019.csv"),
}

# Function to load data using column index
def load_data(file_path, year):
    try:
        df = pd.read_csv(file_path)

        if df.shape[1] < 3:
            st.warning(f"Expected at least 3 columns in {os.path.basename(file_path)}")
            return pd.DataFrame(), None

        # Extract date and measurement from specific columns
        df['Date'] = pd.to_datetime(df.iloc[:, 0], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year

        measurement_col = df.columns[1]  # second column as pollutant
        if "Daily AQI Value" in df.columns:
            df = df[['Date', measurement_col, 'Daily AQI Value', 'Month', 'Year']]
        else:
            df = df[['Date', measurement_col, 'Month', 'Year']]

        return df, measurement_col

    except Exception as e:
        st.warning(f"Error loading {os.path.basename(file_path)}: {e}")
        return pd.DataFrame(), None

# Interface for selection
selected_measurement = st.radio("Select Data Type", ["Measurement", "AQI"])
selected_years = st.multiselect("Select Years", list(file_names.keys()), default=list(file_names.keys()))

# Load selected data
dataframes = []
measurement_column_name = None

for year in selected_years:
    df, pollutant_col = load_data(file_names[year], year)
    if not df.empty:
        dataframes.append(df)
        if measurement_column_name is None:
            measurement_column_name = "Daily AQI Value" if selected_measurement == "AQI" and "Daily AQI Value" in df.columns else pollutant_col

if dataframes:
    all_data = pd.concat(dataframes, ignore_index=True)

    if measurement_column_name not in all_data.columns:
        st.error(f"The selected measurement column '{measurement_column_name}' is not available.")
    else:
        grouped_data = all_data.groupby(['Year', 'Month'])[measurement_column_name].mean().reset_index()

        # Line Chart
        st.subheader(f"Monthly Averages of {measurement_column_name} (Line Plot)")
        fig, ax = plt.subplots(figsize=(10, 6))
        for year in grouped_data['Year'].unique():
            year_data = grouped_data[grouped_data['Year'] == year]
            ax.plot(year_data['Month'], year_data[measurement_column_name], label=str(year))
        ax.set_title(f"Monthly Average {measurement_column_name}")
        ax.set_xlabel("Month")
        ax.set_ylabel(measurement_column_name)
        ax.legend()
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        st.pyplot(fig)

        # Bar and Pie Charts
        if selected_measurement == "Measurement":
            bar_data = all_data.groupby('Year')[measurement_column_name].sum().reset_index()

            st.subheader("Total Pollutant Values by Year (Bar Chart)")
            bar_fig, ax = plt.subplots()
            ax.bar(bar_data['Year'], bar_data[measurement_column_name])
            ax.set_xlabel("Year")
            ax.set_ylabel(f"Total {measurement_column_name}")
            ax.set_title(f"Total {measurement_column_name} by Year")
            st.pyplot(bar_fig)

            st.subheader("Proportion of Pollutant by Year (Pie Chart)")
            pie_fig, ax = plt.subplots()
            ax.pie(bar_data[measurement_column_name], labels=bar_data['Year'], autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Proportion of {measurement_column_name} by Year")
            st.pyplot(pie_fig)

        # Table view
        st.subheader("Grouped Monthly Average Data")
        st.dataframe(grouped_data)

else:
    st.error("No data loaded. Please check file availability or column structure.")
