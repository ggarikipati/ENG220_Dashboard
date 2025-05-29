# ENG-220 Group 021: Environmental Dashboard Project

Link: https://homepagepy-krnegrkwsegbhrfnvpkxqo.streamlit.app/ 

## Overview

This project focuses on building interactive dashboards to analyze and visualize environmental data for **New Mexico**. Our work is divided into three main dashboards, providing insights into air quality, water resources, and their interconnections.

## Dashboards

### 1. Air Quality Dashboard
- **Focus:** Air quality data from 1980 to 2024.
- **Features:**
  - Visualizes air quality trends over time.
  - Displays AQI (Air Quality Index) category distribution.
  - Shows pollutant data by year (e.g., CO, NO2, O3, PM2.5, PM10).
  - Provides summary statistics for selected CBSAs (Core-Based Statistical Areas).
- **Data Source:** [EPA.gov](https://www.epa.gov/) and [Air Quality Monitoring Data](https://waterdata.usgs.gov/monitoring-location/08315500/#period=P7D&showMedian=true&dataTypeId=continuous-00054-0).

### 2. Water Resource Dashboard
- **Focus:** Snow depth and groundwater data in New Mexico.
- **Features:**
  - Yearly trends in snow depth for selected sites.
  - Static water level trends across years.
  - Snow-water level correlations.
  - Regional resource contribution analysis.
  - Identification of top sites with significant resource decline.
- **Data Sources:** [USGS Water Monitoring Data](https://waterdata.usgs.gov/monitoring-location/08315500/#period=P7D&showMedian=true&dataTypeId=continuous-00054-0) and cleaned datasets on snow depth and groundwater levels.

### 3. Correlation Dashboard
- **Focus:** Exploring relationships between air quality and water resource data.
- **Features:**
  - Analyzes environmental interactions across different regions.
  - Highlights potential correlations between snow depth, groundwater levels, and air quality indicators.

## Project Details

This project was developed using **Streamlit** and **Python**. Although group members had no prior Python experience, the code was adapted and edited with assistance from ChatGPT. The dashboards provide interactive and visual insights to help users understand the environmental data better.

### Updates
- **Navigation:** The homepage now includes clear instructions for navigating using the sidebar (accessible via the arrow in the top-left corner).
- **Dashboard Descriptions:** Each dashboard has been clearly described and linked for easy access.
- **Consistent Styling:** The homepage and dashboard buttons have been styled uniformly to enhance user experience.

### Team Members
- **Sumo Alexandre**
- **Ariel Arrellin**
- **Ryan Garcia**
- **Timothy Saucier**
- **Mitchell Snyder**
- **Christian Talamantes**

## How to Run the Dashboards

1. **Install Requirements:**
   - Ensure Python 3.x is installed.
   - Install required libraries:
     ```bash
     pip install streamlit pandas matplotlib
     ```

2. **Run the Dashboards:**
   - Air Quality Dashboard:
     ```bash
     streamlit run app.py
     ```
   - Water Resource Dashboard:
     ```bash
     streamlit run appwater.py
     ```
   - Correlation Dashboard:
     ```bash
     streamlit run correlation.py
     ```

3. **Place Datasets:**
   - Ensure the following files are in the `data` directory:
     - `aqi_combined_1980_2024.csv`
     - `reshaped_snow_depth.csv`
     - `fixed_ground_water_cleaned.csv`

## Data Sources

- **Air Quality Data:** [EPA.gov](https://www.epa.gov/) and [Air Quality Monitoring Data](https://waterdata.usgs.gov/monitoring-location/08315500/#period=P7D&showMedian=true&dataTypeId=continuous-00054-0).
- **Water Resources Data:** [USGS Water Monitoring Data](https://waterdata.usgs.gov/monitoring-location/08315500/#period=P7D&showMedian=true&dataTypeId=continuous-00054-0) and cleaned datasets derived from New Mexico environmental studies.

## Acknowledgments

Special thanks to ChatGPT for aiding in Python coding and streamlining the development process. The dashboards represent a collaborative effort to make environmental data accessible and insightful for a wide audience.

