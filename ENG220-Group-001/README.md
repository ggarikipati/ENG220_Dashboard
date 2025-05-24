# ENG220-Group-001
# Summary of project:
This repository contains the required files for Group 1's final project dashboard for Peace Engineering class, ENG220, during the Fall 2024 term at University of New Mexico.

Our project addressed water supply in the city of Albuquerque and Bernalillo County. We compared water supply and return data to average weather data for Albuquerque. Our data came from USGS, ABCWUA, and NWS. Our dashboard provided an easy way to visualize and compare this data using a Streamlit app we created using python.

___
## Streamlit dashboard application located at:

**[https://eng220-group-001-dashboard.streamlit.app/](https://eng220-group-001-dashboard.streamlit.app/)**

___

## List of files in repository with brief summary:
<details open>
<summary><h3>README.md</h3></summary>

This file.
</details>

___
<details open>
<summary><h3>nm_water_weather_data.csv</h3></summary>
This file contains the preprocessed dataset in csv format for this project. It includes the previous year's data from the following sources:

<details>
<summary><h4>Albuquerque and Bernalillo Country Water Utility Authority (ABCWUA)</h4></summary>

[https://diversionmeter.abcwua.org/Diversion/Home/DiversionMeter](https://diversionmeter.abcwua.org/Diversion/Home/DiversionMeter)

This is the ABCWUA's website containing diversion and recharge data for the San Juan-Chama Drinking Water Project.
</details>

<details>
<summary><h4>United States Geological Service (USGS)</h4></summary>

[https://waterdata.usgs.gov/monitoring-location/08329918/#dataTypeId=continuous-00065-0&period=P7D&showMedian=false](https://waterdata.usgs.gov/monitoring-location/08329918/#dataTypeId=continuous-00065-0&period=P7D&showMedian=false)

[https://waterdata.usgs.gov/monitoring-location/08330875/#dataTypeId=continuous-00065-0&period=P7D&showMedian=false](https://waterdata.usgs.gov/monitoring-location/08330875/#dataTypeId=continuous-00065-0&period=P7D&showMedian=false)

These are the USGS's websites for water level readings of the Rio Grande at the Alameda Bridge and Isleta Lakes respectively.
</details>

<details>
<summary><h4>National Weather Service (NWS)</h4></summary>

[https://www.weather.gov/wrh/climate?wfo=abq](https://www.weather.gov/wrh/climate?wfo=abq)

This is the NWS's page for historical weather data near Albuquerque, New Mexico.
</details>
</details>

___
<details open>
<summary><h3>requirements.txt</h3></summary>
This file contains a list of all necessary libraries and dependencies for the Streamlit application for this project.
</details>

___
<details open>
<summary><h3>water_data_visualization.py</h3></summary>
This file contains the python source code of the Streamlitf application for this project's data visualization dashboard.
</details>

___
