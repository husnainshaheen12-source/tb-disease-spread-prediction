import streamlit as st
import pandas as pd
import plotly.express as px
import time
from pathlib import Path
import sys

sys.path.append(str(Path("src").resolve()))

from live_visual_simulation import generate_live_simulation

st.set_page_config(
    page_title="Live Visual Simulation",
    layout="wide"
)

st.title("Live Visual TB Spread Simulation")

st.markdown("""
This page shows a live visual simulation of TB spread using moving circles.

### Colour Meaning

- Green = Healthy
- Red = Infected
- Blue = Recovered
- Gray/Black = Dead

The system also shows policy alerts when infection becomes serious.
""")

STATUS_ORDER = ["Healthy", "Infected", "Recovered", "Dead"]

COLOR_MAP = {
    "Healthy": "#2ECC71",
    "Infected": "#E74C3C",
    "Recovered": "#3498DB",
    "Dead": "#555555"
}

st.subheader("Simulation Controls")

col1, col2, col3 = st.columns(3)

with col1:
    population_size = st.slider("Population Size", 50, 300, 120, 10)

with col2:
    initial_infected = st.slider("Initial Infected", 1, 50, 12, 1)

with col3:
    days = st.slider("Days", 10, 60, 40, 5)

col4, col5, col6 = st.columns(3)

with col4:
    infection_rate = st.slider("Infection Rate", 0.01, 0.50, 0.30, 0.01)

with col5:
    recovery_rate = st.slider("Recovery Rate", 0.01, 0.30, 0.08, 0.01)

with col6:
    death_rate = st.slider("Death Rate", 0.00, 0.10, 0.03, 0.01)

col7, col8, col9 = st.columns(3)

with col7:
    mask_effect = st.slider("Mask Effect", 0.00, 0.90, 0.30, 0.05)

with col8:
    lockdown_effect = st.slider("Lockdown Effect", 0.00, 0.90, 0.20, 0.05)

with col9:
    hospital_crowd_effect = st.slider("Hospital Crowd Effect", 0.00, 1.00, 0.10, 0.05)

if initial_infected >= population_size:
    st.error("Initial infected must be less than population size.")
    st.stop()

if st.button("Generate Live Visual Simulation"):

    agent_df, summary_df = generate_live_simulation(
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

    summary_df["infected_percent"] = (summary_df["infected"] / population_size) * 100
    summary_df["dead_percent"] = (summary_df["dead"] / population_size) * 100

    max_infected_percent = summary_df["infected_percent"].max()
    final_row = summary_df.iloc[-1]

    st.subheader("Policy Alert")

    outbreak_days = summary_df[summary_df["infected_percent"] >= 5]
    lockdown_days = summary_df[summary_df["infected_percent"] >= 15]
    emergency_days = summary_df[summary_df["infected_percent"] >= 30]

    if len(emergency_days) > 0:
        first_day = int(emergency_days.iloc[0]["day"])
        st.error(
            f"EMERGENCY ALERT: Infection crossed 30% on Day {first_day}. "
            "Strict lockdown, masks, isolation, and treatment are compulsory."
        )
    elif len(lockdown_days) > 0:
        first_day = int(lockdown_days.iloc[0]["day"])
        st.warning(
            f"LOCKDOWN ALERT: Infection crossed 15% on Day {first_day}. "
            "Lockdown and masks are compulsory."
        )
    elif len(outbreak_days) > 0:
        first_day = int(outbreak_days.iloc[0]["day"])
        st.warning(
            f"OUTBREAK DETECTED: Infection crossed 5% on Day {first_day}. "
            "Masks are compulsory and movement should be reduced."
        )
    else:
        st.success("Situation controlled: infection remained below outbreak level.")

    st.subheader("Final Simulation Results")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Healthy", int(final_row["healthy"]))
    m2.metric("Infected", int(final_row["infected"]))
    m3.metric("Recovered", int(final_row["recovered"]))
    m4.metric("Dead", int(final_row["dead"]))

    st.markdown(f"""
### Intervention Settings Used

| Intervention | Value | Meaning |
|---|---:|---|
| Mask Effect | {mask_effect:.2f} | Higher value reduces infection spread |
| Lockdown Effect | {lockdown_effect:.2f} | Higher value reduces movement/contact |
| Recovery Rate | {recovery_rate:.2f} | Higher value helps infected people recover |
| Death Rate | {death_rate:.2f} | Higher value increases death risk |
| Maximum Infection Level | {max_infected_percent:.1f}% | Highest infected percentage during simulation |
""")

    st.subheader("Animated Circle Simulation")
    st.info("Use the play button in the chart to watch people become infected, recovered, or dead over time.")

    legend_rows = []

    for day_value in agent_df["day"].unique():
        for status_value in STATUS_ORDER:
            legend_rows.append({
                "day": day_value,
                "person_id": f"legend_{status_value}_{day_value}",
                "x": -10,
                "y": -10,
                "status": status_value
            })

    legend_df = pd.DataFrame(legend_rows)
    plot_agent_df = pd.concat([agent_df, legend_df], ignore_index=True)

    fig_anim = px.scatter(
        plot_agent_df,
        x="x",
        y="y",
        color="status",
        animation_frame="day",
        animation_group="person_id",
        range_x=[0, 100],
        range_y=[0, 100],
        hover_data=["person_id", "status", "day"],
        title="TB Spread Animation",
        color_discrete_map=COLOR_MAP,
        category_orders={"status": STATUS_ORDER}
    )

    fig_anim.update_traces(
        marker=dict(size=12, opacity=0.90, line=dict(width=1, color="white"))
    )

    fig_anim.update_layout(
        height=650,
        xaxis_title="City X",
        yaxis_title="City Y",
        legend_title="Person Status"
    )

    st.plotly_chart(fig_anim, use_container_width=True)

    st.subheader("Status Trend Over Time")

    summary_long = summary_df.melt(
        id_vars="day",
        value_vars=["healthy", "infected", "recovered", "dead"],
        var_name="status",
        value_name="people"
    )

    fig_line = px.line(
        summary_long,
        x="day",
        y="people",
        color="status",
        markers=True,
        title="Population Status Over Time",
        color_discrete_map={
            "healthy": "#2ECC71",
            "infected": "#E74C3C",
            "recovered": "#3498DB",
            "dead": "#555555"
        }
    )

    st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("Live Step-by-Step Playback")

    play_live = st.checkbox("Play live step-by-step here")
    speed = st.slider("Playback speed seconds per day", 0.05, 0.50, 0.15, 0.05)

    if play_live:
        chart_placeholder = st.empty()
        alert_placeholder = st.empty()
        text_placeholder = st.empty()

        for day_num in sorted(agent_df["day"].unique()):
            day_agents = agent_df[agent_df["day"] == day_num]
            day_summary = summary_df[summary_df["day"] == day_num].iloc[0]
            infected_percent = float(day_summary["infected_percent"])

            if infected_percent >= 30:
                alert_placeholder.error(
                    f"Day {int(day_num)}: Emergency level reached. "
                    "Strict lockdown, masks, isolation, and treatment are compulsory."
                )
            elif infected_percent >= 15:
                alert_placeholder.warning(
                    f"Day {int(day_num)}: Infection is spreading fast. "
                    "Lockdown and masks are compulsory."
                )
            elif infected_percent >= 5:
                alert_placeholder.warning(
                    f"Day {int(day_num)}: Outbreak detected. "
                    "Masks are compulsory and movement should be reduced."
                )
            else:
                alert_placeholder.success(
                    f"Day {int(day_num)}: Situation controlled."
                )

            text_placeholder.markdown(
                f"""
**Day {int(day_num)}**

Healthy: **{int(day_summary['healthy'])}**  
Infected: **{int(day_summary['infected'])}**  
Recovered: **{int(day_summary['recovered'])}**  
Dead: **{int(day_summary['dead'])}**  
Infected Percentage: **{infected_percent:.1f}%**
"""
            )

            day_legend_rows = []

            for status_value in STATUS_ORDER:
                day_legend_rows.append({
                    "day": day_num,
                    "person_id": f"legend_{status_value}_{day_num}",
                    "x": -10,
                    "y": -10,
                    "status": status_value
                })

            day_legend_df = pd.DataFrame(day_legend_rows)
            day_plot_df = pd.concat([day_agents, day_legend_df], ignore_index=True)

            fig_live = px.scatter(
                day_plot_df,
                x="x",
                y="y",
                color="status",
                range_x=[0, 100],
                range_y=[0, 100],
                hover_data=["person_id", "status"],
                title=f"Live Simulation - Day {int(day_num)}",
                color_discrete_map=COLOR_MAP,
                category_orders={"status": STATUS_ORDER}
            )

            fig_live.update_traces(
                marker=dict(size=12, opacity=0.90, line=dict(width=1, color="white"))
            )

            fig_live.update_layout(
                height=550,
                legend_title="Person Status"
            )

            chart_placeholder.plotly_chart(fig_live, use_container_width=True)
            time.sleep(speed)

    st.subheader("Simulation Data")
    st.dataframe(summary_df, use_container_width=True)

else:
    st.info("Set the parameters and click 'Generate Live Visual Simulation'.")
