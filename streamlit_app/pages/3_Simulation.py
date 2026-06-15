import streamlit as st
import pandas as pd
import plotly.express as px
import time
from pathlib import Path
import sys

sys.path.append(str(Path("src").resolve()))

from simulation import run_tb_simulation

st.set_page_config(
    page_title="TB Simulation",
    page_icon="SIM",
    layout="wide"
)

st.title("TB Disease Spread Live Chart Simulation")

st.markdown("""
This page shows a **real live chart simulation**.

When you click **Run Live Simulation**, the chart updates day by day like a video:
Day 1, Day 2, Day 3, and so on.
""")

st.subheader("Simulation Controls")

col1, col2, col3 = st.columns(3)

with col1:
    population_size = st.slider(
        "Total Population",
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
        value=120,
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
        "Recovery Rate",
        min_value=0.01,
        max_value=0.20,
        value=0.04,
        step=0.01
    )

with col6:
    death_rate = st.slider(
        "Death Rate",
        min_value=0.00,
        max_value=0.10,
        value=0.01,
        step=0.005
    )

col7, col8, col9 = st.columns(3)

with col7:
    mask_effect = st.slider(
        "Mask Effect",
        min_value=0.00,
        max_value=0.90,
        value=0.40,
        step=0.05
    )

with col8:
    lockdown_effect = st.slider(
        "Lockdown Effect",
        min_value=0.00,
        max_value=0.90,
        value=0.30,
        step=0.05
    )

with col9:
    hospital_crowd_effect = st.slider(
        "Hospital Crowd Effect",
        min_value=0.00,
        max_value=1.00,
        value=0.20,
        step=0.05
    )

speed = st.slider(
    "Live chart speed seconds per day",
    min_value=0.02,
    max_value=0.50,
    value=0.08,
    step=0.02
)

if initial_infected >= population_size:
    st.error("Initial infected people must be less than total population.")
    st.stop()

if st.button("Run Live Simulation"):

    results_df = run_tb_simulation(
        population_size=population_size,
        initial_infected=initial_infected,
        days=days,
        infection_rate=infection_rate,
        recovery_rate=recovery_rate,
        death_rate=death_rate,
        mask_effect=mask_effect,
        lockdown_effect=lockdown_effect,
        hospital_crowd_effect=hospital_crowd_effect
    )

    st.subheader("Live Simulation Summary")

    day_text_placeholder = st.empty()
    metrics_placeholder = st.empty()
    chart_placeholder = st.empty()

    color_map = {
        "Healthy": "#2ECC71",
        "Current Infected": "#E74C3C",
        "Recovered": "#3498DB",
        "Dead": "#555555"
    }

    for current_day in range(0, days + 1):

        current_df = results_df[results_df["day"] <= current_day].copy()
        current_row = results_df[results_df["day"] == current_day].iloc[0]

        day_text_placeholder.markdown(f"## Current Day: {current_day}")

        with metrics_placeholder.container():
            col_a, col_b, col_c, col_d, col_e = st.columns(5)

            col_a.metric("Total People", int(current_row["total_population"]))
            col_b.metric("Total Ever Infected", int(current_row["total_ever_infected"]))
            col_c.metric("Current Infected", int(current_row["infected"]))
            col_d.metric("Total Recovered", int(current_row["recovered"]))
            col_e.metric("Total Dead", int(current_row["dead"]))

            st.markdown(
                f"""
                **Today:** New Infections = **{int(current_row["daily_new_infections"])}** |
                New Recoveries = **{int(current_row["daily_recoveries"])}** |
                New Deaths = **{int(current_row["daily_deaths"])}**
                """
            )

        chart_df = current_df.melt(
            id_vars="day",
            value_vars=["healthy", "infected", "recovered", "dead"],
            var_name="Status",
            value_name="People"
        )

        status_name_map = {
            "healthy": "Healthy",
            "infected": "Current Infected",
            "recovered": "Recovered",
            "dead": "Dead"
        }

        chart_df["Status"] = chart_df["Status"].map(status_name_map)

        fig = px.line(
            chart_df,
            x="day",
            y="People",
            color="Status",
            markers=True,
            title=f"TB Simulation Live Chart - Day {current_day}",
            color_discrete_map=color_map
        )

        fig.update_layout(
            height=650,
            xaxis_title="Day",
            yaxis_title="Number of People",
            hovermode="x unified",
            legend_title="Status",
            xaxis=dict(range=[0, days]),
            yaxis=dict(range=[0, population_size])
        )

        chart_placeholder.plotly_chart(fig, width="stretch")

        time.sleep(speed)

    st.success("Live simulation completed.")

else:
    st.info("Adjust the controls and click 'Run Live Simulation'.")
