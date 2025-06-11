# Group 005 - California Air Pollution Dashboard

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

# Load Excel files using consistent path pattern
current_dir = os.path.dirname(__file__)
file_paths = {
    "2024": os.path.join(current_dir, "California2024.xlsx"),
    "2023": os.path.join(current_dir, "California2023.xlsx"),
    "2022": os.path.join(current_dir, "California2022.xlsx"),
    "2021": os.path.join(current_dir, "California2021.xlsx"),
    "2020": os.path.join(current_dir, "California2020.xlsx"),
    "2019": os.path.join(current_dir, "California2019.xlsx"),
}

# Measurement descriptions
measurement_info = {
    "CO": "Measured in parts per million (ppm)",
    "Pb": "Measured in micrograms per cubic meter (µg/m³)",
    "NO2": "Measured in parts per billion (ppb)",
    "Ozone": "Measured in parts per million (ppm)",
    "PM2.5": "Measured in micrograms per cubic meter (µg/m³)",
}

# Year-specific fallback measurement columns
fallback_columns = {
    "2024": "Daily Max 1-hour NO2 Concentration",
    "2021": "Daily Max 1-hour NO2 Concentration",
    "2020": "Daily Max 1-hour NO2 Concentration"
}

# Function to load and prepare Excel data
def load_data(file_path, year):
    try:
        df = pd.read_excel(file_path)

        if "Date" not in df.columns:
            st.error(f"No 'Date' column found in {file_path}")
            return pd.DataFrame(), None

        # Identify the appropriate measurement column
        if year in fallback_columns:
            measurement_col = fallback_columns[year]
        else:
            measurement_col = "Daily Mean PM2.5 Concentration" if "Daily Mean PM2.5 Concentration" in df.columns else df.columns[1]

        if measurement_col not in df.columns:
            st.warning(f"'{measurement_col}' not found in {os.path.basename(file_path)}")
            return pd.DataFrame(), None

        df = df[["Date", measurement_col, "Daily AQI Value"]] if "Daily AQI Value" in df.columns else df[["Date", measurement_col]]
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        df = df.dropna(subset=["Date"])
        df["Month"] = df["Date"].dt.month
        df["Year"] = df["Date"].dt.year
        return df, measurement_col

    except Exception as e:
        st.warning(f"Error loading {os.path.basename(file_path)}: {e}")
        return pd.DataFrame(), None

# Sidebar or main UI selections
pollutants = list(measurement_info.keys())
selected_pollutant = st.selectbox("Select Pollutant Sheet", pollutants)
st.markdown(f"**Measurement Info:** {measurement_info[selected_pollutant]}")

measurement_type = st.radio("Select Data Type", ["Measurement", "AQI"])
selected_years = st.multiselect("Select Years", list(file_paths.keys()), default=list(file_paths.keys()))

# Load and combine selected years' data
all_dataframes = []
measurement_colname = None

for year in selected_years:
    df, col = load_data(file_paths[year], year)
    if not df.empty:
        all_dataframes.append(df)
        if measurement_colname is None:
            measurement_colname = col

# Proceed if data is available
if all_dataframes:
    full_data = pd.concat(all_dataframes, ignore_index=True)

    if measurement_type == "AQI":
        measurement_colname = "Daily AQI Value"

    if measurement_colname not in full_data.columns:
        st.error(f"The selected measurement column '{measurement_colname}' is not available.")
    else:
        grouped_data = full_data.groupby(["Year", "Month"])[measurement_colname].mean().reset_index()

        # Line plot
        st.subheader(f"{selected_pollutant} Monthly Averages (Line Plot)")
        fig, ax = plt.subplots(figsize=(10, 6))
        for year in grouped_data["Year"].unique():
            year_data = grouped_data[grouped_data["Year"] == year]
            ax.plot(year_data["Month"], year_data[measurement_colname], label=str(year))
        ax.set_title(f"Monthly Average {measurement_colname}")
        ax.set_xlabel("Month")
        ax.set_ylabel(measurement_colname)
        ax.legend()
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        st.pyplot(fig)

        # Bar + Pie charts only for measurement
        if measurement_type == "Measurement":
            yearly_totals = full_data.groupby("Year")[measurement_colname].sum().reset_index()

            st.subheader(f"Total {measurement_colname} by Year (Bar Chart)")
            bar_fig, ax = plt.subplots()
            ax.bar(yearly_totals["Year"], yearly_totals[measurement_colname])
            ax.set_title(f"Total {selected_pollutant} by Year")
            ax.set_xlabel("Year")
            ax.set_ylabel(f"Total {measurement_colname}")
            st.pyplot(bar_fig)

            st.subheader(f"Proportion of {measurement_colname} by Year (Pie Chart)")
            pie_fig, ax = plt.subplots()
            ax.pie(yearly_totals[measurement_colname], labels=yearly_totals["Year"], autopct="%1.1f%%", startangle=90)
            ax.set_title(f"Yearly Proportion of {measurement_colname}")
            st.pyplot(pie_fig)

        st.subheader("Grouped Monthly Average Data")
        st.dataframe(grouped_data)

else:
    st.error("No data loaded. Please check file format, column names, or selections.")
