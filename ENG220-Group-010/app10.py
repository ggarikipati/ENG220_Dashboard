# -*- coding: utf-8 -*-
# Group 010 - Gun Violence Data Dashboard

import streamlit as st
import pandas as pd
import os

# Title
st.title("Group-010")

st.markdown("""
### Gun Violence Data Visualization

**Project Summary**  
Our project explores how **cross-agency collaboration impacts gun violence in New Mexico**.  
It focuses on community-based programs and government partnerships that work to reduce firearm-related incidents through outreach, legislation, and enforcement.  

The dataset includes:
- Incidents involving gun violence
- Firearms seized
- Arrests and deaths related to firearms

The app presents insights into trends across **time, gender, geography, and community dynamics**.

---
""")

# Load large CSV from GitHub
@st.cache_data
def read_large_csv():
    file_url = "https://raw.githubusercontent.com/BlassMolina03/ENG-220-MATLAB-PROJECTS/main/Data%20Sheet%201.csv"
    try:
        chunk_size = 1000
        chunks = pd.read_csv(file_url, encoding="ISO-8859-1", sep=",", on_bad_lines="skip", chunksize=chunk_size)
        df = pd.concat([chunk for chunk in chunks], ignore_index=True)
        return df.dropna()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Read and prepare data
df = read_large_csv()

if df is not None:
    # Clean and preprocess
    df['Incident Date'] = pd.to_datetime(df['Incident Date'], errors='coerce')
    df.dropna(subset=['Incident Date'], inplace=True)
    df['day_of_week'] = df['Incident Date'].dt.day_name()

    st.subheader("Cleaned Data Preview")
    st.dataframe(df)

    # Dropdown to select visualization type
    graph_choice = st.selectbox("Choose Visualization", [
        "Monthly Increase", "Gender Analysis", "Incidents by City or County", "Incidents by Date"
    ])

    # Prepare analysis columns
    df['month_year'] = df['Incident Date'].dt.to_period('M')
    monthly_counts = df['month_year'].value_counts().sort_index()
    gender_counts = df['Participant Gender'].value_counts()
    city_or_county_counts = df['City Or County'].value_counts()
    date_counts = df['Incident Date'].dt.date.value_counts().sort_index()

    # Render chart
    if graph_choice == "Monthly Increase":
        st.subheader("Monthly Increase of Gun Violence Incidents")
        st.line_chart(monthly_counts)
        st.caption("This chart shows how gun violence trends have changed month-to-month.")

    elif graph_choice == "Gender Analysis":
        st.subheader("Incidents by Gender")
        st.bar_chart(gender_counts)
        st.caption("This chart shows the number of incidents categorized by participant gender.")

    elif graph_choice == "Incidents by City or County":
        st.subheader("Incidents by City or County")
        st.bar_chart(city_or_county_counts)
        st.caption("This chart shows the number of incidents recorded per city or county.")

    elif graph_choice == "Incidents by Date":
        st.subheader("Incidents by Date")
        st.line_chart(date_counts)
        st.caption("This chart shows the daily incident distribution over time.")

else:
    st.error("Data could not be loaded from the source.")
