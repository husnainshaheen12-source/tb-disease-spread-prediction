import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

# Add src folder to Python path
sys.path.append(str(Path("src").resolve()))

from simulation import run_tb_simulation

st.set_page_config(
    page_title="TB Simulation",
    page_icon="SIM",
    layout="wide"
)

st.title("TB Disease Spread Simulation")

st.markdown("""
This page simulates the spread of Tuberculosis in a population.

The simulation includes:

- Healthy people
- Infected people
- Recovered / treated people
- Mask effect
- Lockdown effect
- Treatment / recovery effect
- Hospital crowd effect

This is a simplified educational simulation and does not represent exact real-world medical transmission.
""")

st.subheader("Simulation Controls")

col1, col2, col3 = st.columns(3)

with col1:
    population_size = st.slider(
        "Population Size",
        min_value=100,
        max_value=5000,
        value=500,
        step=100
    )

with col2:
    initial_infected = st.slider(
        "Initial Infected People",
        min_value=1,
        max_value=200,
        value=10,
        step=1
    )

with col3:
    days = st.slider(
        "Number of Days",
        min_value=10,
        max_value=365,
        value=60,
        step=5
    )

col4, col5, col6 = st.columns(3)

with col4:
    infection_rate = st.slider(
        "Infection Rate",
        min_value=0.01,
        max_value=0.30,
        value=0.08,
        step=0.01
    )

with col5:
    recovery_rate = st.slider(
        "Recovery / Treatment Rate",
        min_value=0.01,
        max_value=0.20,
        value=0.04,
        step=0.01
    )

with col6:
    mask_effect = st.slider(
        "Mask Effect",
        min_value=0.00,
        max_value=0.90,
        value=0.40,
        step=0.05
    )

col7, col8 = st.columns(2)

with col7:
    lockdown_effect = st.slider(
        "Lockdown Effect",
        min_value=0.00,
        max_value=0.90,
        value=0.30,
        step=0.05
    )

with col8:
    hospital_crowd_effect = st.slider(
        "Hospital Crowd Effect",
        min_value=0.00,
        max_value=1.00,
        value=0.20,
        step=0.05
    )

if initial_infected >= population_size:
    st.error("Initial infected people must be less than population size.")
    st.stop()

if st.button("Run Simulation"):
    results_df = run_tb_simulation(
        population_size=population_size,
        initial_infected=initial_infected,
        days=days,
        infection_rate=infection_rate,
        recovery_rate=recovery_rate,
        mask_effect=mask_effect,
        lockdown_effect=lockdown_effect,
        hospital_crowd_effect=hospital_crowd_effect
    )

    st.subheader("Simulation Results")

    final_row = results_df.iloc[-1]

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric("Final Healthy", int(final_row["healthy"]))
    metric2.metric("Final Infected", int(final_row["infected"]))
    metric3.metric("Final Recovered", int(final_row["recovered"]))

    plot_df = results_df.melt(
        id_vars="day",
        value_vars=["healthy", "infected", "recovered"],
        var_name="Status",
        value_name="People"
    )

    fig = px.line(
        plot_df,
        x="day",
        y="People",
        color="Status",
        title="TB Disease Spread Simulation Over Time",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Simulation Data Table")
    st.dataframe(results_df, use_container_width=True)

    csv = results_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Simulation Results CSV",
        data=csv,
        file_name="tb_simulation_results.csv",
        mime="text/csv"
    )
else:
    st.info("Adjust the simulation controls and click 'Run Simulation'.")
