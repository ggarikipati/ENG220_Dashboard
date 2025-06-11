
import streamlit as st

st.title("Group-019")

st.markdown("""
### Project Overview

This repository contains two distinct types of CSV files, each offering valuable insights into clean energy resources and health-related grants awarded to Santa Fe, New Mexico.

---

#### Clean Energy Source Analysis

The **EPI dataset** focuses on clean energy stock indices. It includes data from companies specializing in clean energy, featuring variables like average annual stock prices and trends in New Mexico.

- During the COVID-19 pandemic, government subsidies shifted away from clean energy to prioritize health.
- Post-pandemic, clean energy stocks rebounded as funding resumed.
- In contrast, **non-clean energy sectors** (like electricity) saw temporary boosts during lockdowns due to higher demand but later declined.

---

#### Health Grant Analysis

The **CDC dataset** includes information on federal health grants awarded to Santa Fe.

- A sharp increase in funding during the pandemic emphasized health priorities.
- The focus was on **emerging disease response**, **STI prevention**, and **respiratory immunization**.
- Funding decreased post-pandemic as emergency health priorities stabilized.

---

#### Conclusion

This project highlights how uncontrollable events like the COVID-19 pandemic can drastically reshape public funding priorities. Government intervention plays a critical role in:

- Steering support between clean and non-clean energy initiatives.
- Driving health investments in response to emergencies.

Explore the visualizations in the sections below to dive deeper into the funding trends and implications.

""")
