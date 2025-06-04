import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Title
st.title("Group-011")

st.markdown("""
### Gun Violence Trends in Albuquerque and New Mexico

This project investigates **gun violence in Albuquerque** and across **New Mexico**, aiming to identify patterns by location, year, age, race, and gender.  
The goal is to inform interventions and resource allocation to reduce firearm-related deaths.

From **2008 to 2021**, gun-related deaths in New Mexico rose from **283 deaths (14.1 per 100,000)** to **562 deaths (27 per 100,000)**.  
By analyzing demographic and geographic data, we hope to guide **policy**, **law enforcement**, and **community efforts** through data-driven action.

---
""")

# Main interface dropdown (instead of sidebar)
graph_type = st.selectbox(
    "Select a Graph to View",
    [
        "Graph 1: Firearm Injury Death by Year (New Mexico and U.S.)",
        "Graph 2: Gun Violence for Counties in New Mexico",
        "Graph 3: Gun Violence Rates Per Year",
        "Graph 4: Gun Violence for Race and Gender",
        "Graph 5: Gun Violence for Age and Gender",
    ]
)

# Set current directory for file access
current_dir = os.path.dirname(__file__)

# Graph 1
if graph_type == "Graph 1: Firearm Injury Death by Year (New Mexico and U.S.)":
    st.subheader("Firearm Injury Death by Year")
    file_path = os.path.join(current_dir, 'Firearm Injury Death by Year, New Mexico and U.S.csv')

    try:
        data = pd.read_csv(file_path)
        st.dataframe(data)

        y_column = st.selectbox("Select Y-axis column", [
            "Deaths per 100,000 Population, Age-adjusted",
            "Gun Casualties Per Year",
            "Population Count Estimate"
        ])

        if st.button("Plot Graph"):
            fig, ax = plt.subplots()
            ax.bar(data["Year"], data[y_column])
            ax.set_title(f"{y_column} by Year")
            ax.set_xlabel("Year")
            ax.set_ylabel(y_column)
            plt.xticks(rotation=45)
            st.pyplot(fig)

    except FileNotFoundError:
        st.error("CSV file not found. Please check the filename and location.")

# Graph 2
elif graph_type == "Graph 2: Gun Violence for Counties in New Mexico":
    st.subheader("Gun Violence by County")
    file_path = os.path.join(current_dir, 'Gun Violence for Counties.csv')

    try:
        data = pd.read_csv(file_path)
        st.dataframe(data)

        y_column = st.selectbox("Select Y-axis column", [
            "Deaths per 100,000 Population",
            "Gun Casualties",
            "Population Count Estimate"
        ])

        if st.button("Plot Graph"):
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(data["County"], data[y_column])
            ax.set_title(f"{y_column} by County")
            ax.set_xlabel("County")
            ax.set_ylabel(y_column)
            plt.xticks(rotation=90)
            st.pyplot(fig)

    except FileNotFoundError:
        st.error("CSV file not found. Please check the filename and location.")

# Graph 3
elif graph_type == "Graph 3: Gun Violence Rates Per Year":
    st.subheader("Gun Violence Rates by Year")
    file_path = os.path.join(current_dir, 'Gun Violence Rates Per Year.csv')

    try:
        data = pd.read_csv(file_path)
        st.dataframe(data)

        y_column = st.selectbox("Select Y-axis column", [
            "Total Gun Death Rate",
            "Gun Homicide Rate",
            "Gun Suicide Rate"
        ])

        if st.button("Plot Graph"):
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(data["Year"], data[y_column], marker='o')
            ax.set_title(f"{y_column} by Year")
            ax.set_xlabel("Year")
            ax.set_ylabel(y_column)
            plt.xticks(rotation=45)
            st.pyplot(fig)

    except FileNotFoundError:
        st.error("CSV file not found. Please check the filename and location.")

# Graph 4
elif graph_type == "Graph 4: Gun Violence for Race and Gender":
    st.subheader("Gun Violence by Race and Gender")
    file_path = os.path.join(current_dir, 'Gun Violence For Race and Gender.csv')

    try:
        data = pd.read_csv(file_path)
        st.dataframe(data)

        sex = st.selectbox("Select Sex", ["Male", "Female", "Both"])
        filtered_data = data[data["Sex"] == sex]

        metric = st.selectbox("Select Metric", [
            "Deaths per 100,000 Population, Age-adjusted",
            "Count",
            "Population Count Estimate"
        ])

        if st.button("Plot Graph"):
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(filtered_data["Race/Ethnicity"], filtered_data[metric])
            ax.set_title(f"{metric} by Race/Ethnicity ({sex})")
            ax.set_xlabel("Race/Ethnicity")
            ax.set_ylabel(metric)
            plt.xticks(rotation=45)
            st.pyplot(fig)

    except FileNotFoundError:
        st.error("CSV file not found. Please check the filename and location.")

# Graph 5
elif graph_type == "Graph 5: Gun Violence for Age and Gender":
    st.subheader("Gun Violence by Age and Gender")
    file_path = os.path.join(current_dir, 'Gun Violence For Age And Gender.csv')

    try:
        data = pd.read_csv(file_path)
        st.dataframe(data)

        sex = st.selectbox("Select Sex", ["Male", "Female", "Both"])
        filtered_data = data[data["Sex"] == sex]

        metric = st.selectbox("Select Metric", [
            "Deaths per 100,000 Population",
            "Gun Casualities",
            "Population Count Estimate"
        ])

        if st.button("Plot Graph"):
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(filtered_data["Age Group"], filtered_data[metric])
            ax.set_title(f"{metric} by Age Group ({sex})")
            ax.set_xlabel("Age Group")
            ax.set_ylabel(metric)
            plt.xticks(rotation=45)
            st.pyplot(fig)

    except FileNotFoundError:
        st.error("CSV file not found. Please check the filename and location.")
