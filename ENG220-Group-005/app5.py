import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")
st.markdown("""
### California PM2.5 Dashboard

Visualize **PM2.5 Air Pollution Data** from 2019–2024 using CSV files.  
Includes **monthly averages**, **year-wise totals**, and **AQI comparisons**.
""")

# File setup
base_path = os.path.dirname(__file__)
file_names = {
    "2024": os.path.join(base_path, "California2024.csv"),
    "2023": os.path.join(base_path, "California2023.csv"),
    "2022": os.path.join(base_path, "California2022.csv"),
    "2021": os.path.join(base_path, "California2021.csv"),
    "2020": os.path.join(base_path, "California2020.csv"),
    "2019": os.path.join(base_path, "California2019.csv"),
}

# Sidebar options
selected_years = st.sidebar.multiselect("Select Years", list(file_names.keys()), default=list(file_names.keys()))
metric = st.sidebar.radio("View By", ["PM2.5 Concentration", "AQI"])

# Load function
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
        df.dropna(subset=["Date"], inplace=True)
        df["Month"] = df["Date"].dt.month
        df["Year"] = df["Date"].dt.year
        return df
    except Exception as e:
        st.error(f"Error loading {filepath}: {e}")
        return pd.DataFrame()

# Load data
frames = []
for year in selected_years:
    df = load_data(file_names[year])
    if not df.empty:
        frames.append(df)

# Visualizations
if frames:
    full_df = pd.concat(frames)

    col_name = "Daily Mean PM2.5 Concentration" if metric == "PM2.5 Concentration" else "Daily AQI Value"
    if col_name not in full_df.columns:
        st.error(f"Column '{col_name}' not found in the files.")
    else:
        grouped = full_df.groupby(["Year", "Month"])[col_name].mean().reset_index()

        st.subheader(f"Monthly Average {col_name}")
        fig, ax = plt.subplots(figsize=(10, 6))
        for year in grouped["Year"].unique():
            subset = grouped[grouped["Year"] == year]
            ax.plot(subset["Month"], subset[col_name], label=str(year))
        ax.set_title(f"Monthly Average {col_name}")
        ax.set_xlabel("Month")
        ax.set_ylabel(col_name)
        ax.legend()
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        st.pyplot(fig)

        st.subheader("Monthly Average Table")
        st.dataframe(grouped)

        # Bar chart: yearly sum
        st.subheader(f"Total {col_name} by Year")
        yearly_sum = full_df.groupby("Year")[col_name].sum().reset_index()
        fig2, ax2 = plt.subplots()
        ax2.bar(yearly_sum["Year"], yearly_sum[col_name])
        ax2.set_xlabel("Year")
        ax2.set_ylabel(f"Total {col_name}")
        ax2.set_title(f"Total {col_name} by Year")
        st.pyplot(fig2)

else:
    st.warning("No data loaded. Please check file names or date format.")
