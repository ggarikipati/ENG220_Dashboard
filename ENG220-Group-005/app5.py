import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os


# Title and markdown
st.title("Group-005")

st.markdown("""
### California Air Pollution Visualization Dashboard

This app provides an interactive interface to explore **California air quality data** from **2019 to 2024**, 
integrated with Streamlit for intuitive exploration.  
Data includes daily readings of various pollutants like **CO, NO₂, Ozone, PM2.5, and Lead**, sourced from government monitoring systems.  
You can compare pollutants by year, visualize monthly averages, and explore proportions via bar and pie charts.
""")

# File directory and filenames
base_path = os.path.dirname(__file__)
years = ["2024", "2023", "2022", "2021", "2020", "2019"]
file_paths = {year: os.path.join(base_path, f"California{year}.csv") for year in years}

pollutants = ["CO", "Pb", "NO2", "Ozone", "PM2.5"]
measurement_info = {
    "CO": "Measured in parts per million (ppm)",
    "Pb": "Measured in µg/m³",
    "NO2": "Measured in parts per billion (ppb)",
    "Ozone": "Measured in parts per million (ppm)",
    "PM2.5": "Measured in µg/m³"
}

# UI selections
selected_pollutant = st.selectbox("Select Pollutant", pollutants)
st.markdown(f"**Measurement Info:** {measurement_info[selected_pollutant]}")

measurement_options = ["Measurement"]
if selected_pollutant != "Pb":
    measurement_options.append("AQI")
selected_measurement = st.radio("Select Data Type", measurement_options)

selected_years = st.multiselect("Select Years", years, default=years)

# Load data
dataframes = []
measurement_column = selected_pollutant if selected_measurement == "Measurement" else "Daily AQI Value"

for year in selected_years:
    path = file_paths[year]
    try:
        df = pd.read_csv(path)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)
        if measurement_column in df.columns:
            df = df[['Date', measurement_column]].copy()
            df['Year'] = df['Date'].dt.year
            df['Month'] = df['Date'].dt.month
            dataframes.append(df)
    except Exception as e:
        st.warning(f"Could not load {path}: {e}")

if dataframes:
    combined_df = pd.concat(dataframes, ignore_index=True)

    grouped_data = combined_df.groupby(['Year', 'Month'])[measurement_column].mean().reset_index()

    # Line chart
    st.subheader(f"{selected_pollutant} Monthly Averages (Line Plot)")
    fig, ax = plt.subplots(figsize=(10, 6))
    for year in grouped_data['Year'].unique():
        year_data = grouped_data[grouped_data['Year'] == year]
        ax.plot(year_data['Month'], year_data[measurement_column], label=str(year))
    ax.set_title(f"Monthly Average {measurement_column} for {selected_pollutant}")
    ax.set_xlabel("Month")
    ax.set_ylabel(measurement_column)
    ax.legend()
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    st.pyplot(fig)

    if selected_measurement == "Measurement":
        bar_data = combined_df.groupby('Year')[measurement_column].sum().reset_index()

        st.subheader(f"Total {selected_pollutant} Values by Year (Bar Chart)")
        fig_bar, ax = plt.subplots()
        ax.bar(bar_data['Year'], bar_data[measurement_column])
        ax.set_xlabel("Year")
        ax.set_ylabel(f"Total {measurement_column}")
        ax.set_title(f"Total {selected_pollutant} by Year")
        st.pyplot(fig_bar)

        st.subheader(f"Proportion of {selected_pollutant} Values by Year (Pie Chart)")
        fig_pie, ax = plt.subplots()
        ax.pie(bar_data[measurement_column], labels=bar_data['Year'], autopct='%1.1f%%', startangle=90)
        ax.set_title(f"Proportion of Total {measurement_column} by Year")
        st.pyplot(fig_pie)

    st.subheader("Grouped Monthly Average Data")
    st.dataframe(grouped_data)
else:
    st.error("No data loaded. Ensure selected files exist and include the selected pollutant column.")
