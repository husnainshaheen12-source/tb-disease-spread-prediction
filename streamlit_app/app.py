import streamlit as st

st.set_page_config(
    page_title="TB Spread Prediction System",
    page_icon="??",
    layout="wide"
)

st.title("AI-Based Tuberculosis Spread Simulation and TB Case Prediction System")

st.markdown("""
## Project Overview

Tuberculosis, also known as TB, is a bacterial infectious disease that mainly spreads through the air when an infected person coughs, sneezes, or stays in close contact with other people.

This project uses:

- **Dataset Analysis**
- **Machine Learning**
- **Disease Spread Simulation**
- **Streamlit Dashboard**

to study TB trends and predict future TB cases.
""")

st.markdown("""
## Project Objectives

1. Analyze real-world TB data.
2. Identify TB trends by country and year.
3. Train machine learning models to predict TB cases.
4. Simulate TB spread in a population.
5. Build an interactive dashboard for users.
""")

st.markdown("""
## Project Modules

| Module | Description |
|---|---|
| Dataset Analysis | Shows TB cases, incidence, and country-level trends |
| Machine Learning | Predicts estimated TB cases |
| Simulation | Simulates TB disease spread |
| Dashboard | Interactive Streamlit web app |
""")

st.success("Dashboard Home Page Loaded Successfully!")

st.info("Use the sidebar pages later to explore data analysis, prediction, and simulation.")
