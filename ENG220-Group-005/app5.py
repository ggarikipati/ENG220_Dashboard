
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ✅ Must be the first Streamlit command
st.set_page_config(page_title="Group-005", layout="wide")

# Title
st.title("Group-005")

# Markdown description
st.markdown("""
### California Air Pollution Visualization Dashboard

This app provides an interactive interface to explore **California air quality data** from **2019 to 2024**, 
integrated with Streamlit for intuitive exploration.  
You can compare pollutants by year, visualize monthly averages, and explore proportions via bar and pie charts.
""")

# File paths (CSV)
base_path = os.path.dirname(__file__)
file_names = {
    "2024": os.path.join(base_path, "California2024.csv"),
    "2023": os.path.join(base_path, "California2023.csv"),
    "2022": os.path.join(base_path, "California2022.csv"),
    "2021": os.path.join(base_path, "California2021.csv"),
    "2020": os.path.join(base_path, "California2020.csv"),
    "2019": os.path.join(base_path, "California2019.csv"),
}

# Define pollutant options and corresponding fallback column names
pollutant_columns = {
    "PM2.5": ["Daily Mean PM2.5 Concentration", "Daily Max 1-hour NO2 Concentration"],
    "NO2": ["Daily Max 1-hour NO2 Concentration"],
}

aqi_column = "Daily AQI Value"

# Load CSV and return correct column based on pollutant fallback list
def load_data(file_path, fallback_columns):
    try:
        df = pd.read_csv(file_path)
        for col in fallback_columns:
            if col in df.columns:
                measurement_col = col
                break
        else:
            st.warning(f"No matching column found in {os.path.basename(file_path)}")
            return pd.DataFrame(), None

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        return df, measurement_col
    except Exception as e:
        st.error(f"Error loading {os.path.basename(file_path)}: {e}")
        return pd.DataFrame(), None

# --- UI ---
selected_pollutant = st.selectbox("Select Pollutant", list(pollutant_columns.keys()))
measurement_options = ["Measurement", "AQI"]
selected_measurement = st.radio("Select Data Type", measurement_options)
selected_years = st.multiselect("Select Years", list(file_names.keys()), default=list(file_names.keys()))

# --- Load and process data ---
dataframes = []
measurement_column_name = None

for year in selected_years:
    df, col = load_data(file_names[year], pollutant_columns[selected_pollutant])
    if not df.empty:
        if selected_measurement == "AQI":
            if aqi_column not in df.columns:
                st.warning(f"{aqi_column} not found in {year} file.")
                continue
            df[aqi_column] = pd.to_numeric(df[aqi_column], errors='coerce')
        else:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        dataframes.append(df)
        if measurement_column_name is None:
            measurement_column_name = aqi_column if selected_measurement == "AQI" else col

if dataframes:
    all_data = pd.concat(dataframes, ignore_index=True)
    measurement_col = measurement_column_name

    if measurement_col not in all_data.columns:
        st.error(f"'{measurement_col}' column missing in combined data.")
    else:
        grouped_data = all_data.groupby(['Year', 'Month'])[measurement_col].mean().reset_index()

        # Line Plot
        st.subheader(f"{selected_pollutant} Monthly Averages (Line Plot)")
        fig, ax = plt.subplots(figsize=(10, 6))
        for year in grouped_data['Year'].unique():
            data = grouped_data[grouped_data['Year'] == year]
            ax.plot(data['Month'], data[measurement_col], label=str(year))
        ax.set_title(f"Monthly Average of {measurement_col}")
        ax.set_xlabel("Month")
        ax.set_ylabel(measurement_col)
        ax.legend()
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        st.pyplot(fig)

        # Bar + Pie
        if selected_measurement == "Measurement":
            bar_data = all_data.groupby('Year')[measurement_col].sum().reset_index()

            st.subheader(f"Total {selected_pollutant} by Year (Bar Chart)")
            bar_fig, ax = plt.subplots()
            ax.bar(bar_data['Year'], bar_data[measurement_col])
            ax.set_xlabel("Year")
            ax.set_ylabel("Total")
            ax.set_title(f"{selected_pollutant} Total by Year")
            st.pyplot(bar_fig)

            st.subheader(f"Proportion of {selected_pollutant} by Year (Pie Chart)")
            pie_fig, ax = plt.subplots()
            ax.pie(bar_data[measurement_col], labels=bar_data['Year'], autopct='%1.1f%%', startangle=90)
            ax.set_title(f"Proportional Distribution of {selected_pollutant}")
            st.pyplot(pie_fig)

        st.subheader("Grouped Monthly Average Data")
        st.dataframe(grouped_data)
else:
    st.error("No data loaded. Please check file names or pollutant selection.")
