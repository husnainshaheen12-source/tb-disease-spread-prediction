import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import streamlit.components.v1 as components
from pathlib import Path
import sys
from styles import apply_custom_style, page_header

sys.path.append(str(Path("src").resolve()))

from simulation import run_tb_simulation

st.set_page_config(
    page_title="Live Visual Simulation",
    page_icon="🟢",
    layout="wide"
)

apply_custom_style()

page_header(
    title="Live Visual TB Spread Simulation",
    subtitle="View the TB simulation using moving dots that represent healthy, infected, recovered, and dead people.",
    badge="Live Visualisation"
)

st.markdown("""
This page uses the **same simulation calculation** as the Simulation page.

The difference is only the display:

- Simulation page shows the result using a live chart.
- Live Visual Simulation page shows the same result using moving dots.

So both pages show the same total infected, recovered, and dead numbers.
""")

st.markdown("""
### Colour Meaning

- Green = Healthy
- Red = Infected
- Blue = Recovered
- Gray/Black = Dead
""")

STATUS_ORDER = ["Healthy", "Infected", "Recovered", "Dead"]

COLOR_MAP = {
    "Healthy": "#2ECC71",
    "Infected": "#E74C3C",
    "Recovered": "#3498DB",
    "Dead": "#777777"
}

st.subheader("Simulation Controls")

col1, col2, col3 = st.columns(3)

with col1:
    population_size = st.slider("Total Population", 100, 5000, 500, 100)

with col2:
    initial_infected = st.slider("Initial Infected People", 1, 200, 10, 1)

with col3:
    days = st.slider("Number of Days", 10, 365, 120, 5)

col4, col5, col6 = st.columns(3)

with col4:
    infection_rate = st.slider("Infection Rate", 0.01, 0.30, 0.08, 0.01)

with col5:
    recovery_rate = st.slider("Recovery Rate", 0.01, 0.20, 0.04, 0.01)

with col6:
    death_rate = st.slider("Death Rate", 0.00, 0.10, 0.01, 0.005)

col7, col8, col9 = st.columns(3)

with col7:
    mask_effect = st.slider("Mask Effect", 0.00, 0.90, 0.40, 0.05)

with col8:
    lockdown_effect = st.slider("Lockdown Effect", 0.00, 0.90, 0.30, 0.05)

with col9:
    hospital_crowd_effect = st.slider("Hospital Crowd Effect", 0.00, 1.00, 0.20, 0.05)

speed = st.slider("Animation speed milliseconds per day", 50, 500, 120, 10)

if initial_infected >= population_size:
    st.error("Initial infected people must be less than total population.")
    st.stop()


def build_moving_dot_frames(results_df, population_size, lockdown_effect):
    rng = np.random.default_rng(42)

    x_positions = rng.uniform(0, 100, population_size)
    y_positions = rng.uniform(0, 100, population_size)

    status = np.array(["Healthy"] * population_size, dtype=object)

    initial_infected_count = int(results_df.iloc[0]["infected"])
    infected_people = rng.choice(population_size, initial_infected_count, replace=False)
    status[infected_people] = "Infected"

    movement_step = max(0.8, 5.0 * (1 - lockdown_effect))

    all_rows = []

    for _, row in results_df.iterrows():
        day = int(row["day"])

        if day > 0:
            new_infections = int(row["daily_new_infections"])
            new_recoveries = int(row["daily_recoveries"])
            new_deaths = int(row["daily_deaths"])

            healthy_ids = np.where(status == "Healthy")[0]

            if len(healthy_ids) > 0 and new_infections > 0:
                chosen = rng.choice(
                    healthy_ids,
                    min(new_infections, len(healthy_ids)),
                    replace=False
                )
                status[chosen] = "Infected"

            infected_ids = np.where(status == "Infected")[0]

            if len(infected_ids) > 0 and new_deaths > 0:
                chosen = rng.choice(
                    infected_ids,
                    min(new_deaths, len(infected_ids)),
                    replace=False
                )
                status[chosen] = "Dead"

            infected_ids = np.where(status == "Infected")[0]

            if len(infected_ids) > 0 and new_recoveries > 0:
                chosen = rng.choice(
                    infected_ids,
                    min(new_recoveries, len(infected_ids)),
                    replace=False
                )
                status[chosen] = "Recovered"

        alive_mask = status != "Dead"

        x_positions[alive_mask] = np.clip(
            x_positions[alive_mask] + rng.uniform(-movement_step, movement_step, alive_mask.sum()),
            0,
            100
        )

        y_positions[alive_mask] = np.clip(
            y_positions[alive_mask] + rng.uniform(-movement_step, movement_step, alive_mask.sum()),
            0,
            100
        )

        for person_id in range(population_size):
            all_rows.append({
                "day": day,
                "person_id": person_id,
                "x": x_positions[person_id],
                "y": y_positions[person_id],
                "status": status[person_id]
            })

    return pd.DataFrame(all_rows)


if st.button("Generate Live Visual Simulation"):

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

    final_row = results_df.iloc[-1]

    st.subheader("Final Simulation Summary")

    m1, m2, m3, m4, m5 = st.columns(5)

    m1.metric("Total People", int(final_row["total_population"]))
    m2.metric("Total Ever Infected", int(final_row["total_ever_infected"]))
    m3.metric("Current Infected", int(final_row["infected"]))
    m4.metric("Total Recovered", int(final_row["recovered"]))
    m5.metric("Total Dead", int(final_row["dead"]))

    results_df["infected_percent"] = (results_df["infected"] / population_size) * 100

    outbreak_days = results_df[results_df["infected_percent"] >= 5]
    lockdown_days = results_df[results_df["infected_percent"] >= 15]
    emergency_days = results_df[results_df["infected_percent"] >= 30]

    st.subheader("Policy Alert")

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

    st.subheader("Smooth Moving Dot Simulation")
    st.info("Dots move smoothly with a dark background. Dead dots stop moving.")

    dot_frames_df = build_moving_dot_frames(
        results_df=results_df,
        population_size=population_size,
        lockdown_effect=lockdown_effect
    )

    marker_size = 8
    if population_size >= 1000:
        marker_size = 5
    if population_size >= 3000:
        marker_size = 3

    dummy_rows = []

    for day_value in sorted(dot_frames_df["day"].unique()):
        for status_name in STATUS_ORDER:
            dummy_rows.append({
                "day": day_value,
                "person_id": f"dummy_{status_name}_{day_value}",
                "x": -10,
                "y": -10,
                "status": status_name
            })

    dot_frames_df = pd.concat(
        [dot_frames_df, pd.DataFrame(dummy_rows)],
        ignore_index=True
    )

    dot_frames_df["status"] = pd.Categorical(
        dot_frames_df["status"],
        categories=STATUS_ORDER,
        ordered=True
    )

    fig = px.scatter(
        dot_frames_df,
        x="x",
        y="y",
        color="status",
        animation_frame="day",
        animation_group="person_id",
        range_x=[0, 100],
        range_y=[0, 100],
        hover_data=["person_id", "status", "day"],
        title="Smooth Moving Dot TB Simulation",
        color_discrete_map=COLOR_MAP,
        category_orders={"status": STATUS_ORDER},
        template="plotly_dark"
    )

    fig.update_traces(
        marker=dict(size=marker_size, opacity=0.95, line=dict(width=1, color="white"))
    )

    fig.update_layout(
        height=700,
        xaxis_title="City X",
        yaxis_title="City Y",
        legend_title="Person Status",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="white"),
        xaxis=dict(gridcolor="#333333"),
        yaxis=dict(gridcolor="#333333")
    )

    fig.update_layout(updatemenus=[], sliders=[])

    html_chart = fig.to_html(
        include_plotlyjs="cdn",
        full_html=False,
        auto_play=False,
        div_id="smooth_dot_simulation",
        config={"displayModeBar": False}
    )

    autoplay_script = f"""
    <script>
    setTimeout(function() {{
        var chart = document.getElementById("smooth_dot_simulation");
        if (chart) {{
            Plotly.animate(chart, null, {{
                frame: {{duration: {speed}, redraw: false}},
                transition: {{duration: {speed}, easing: "linear"}},
                mode: "immediate"
            }});
        }}
    }}, 700);
    </script>
    """

    components.html(
        html_chart + autoplay_script,
        height=760,
        scrolling=False
    )

    st.subheader("Day-by-Day Simulation Table")

    display_df = results_df.rename(columns={
        "day": "Day",
        "healthy": "Healthy",
        "infected": "Infected",
        "recovered": "Recovered",
        "dead": "Dead",
        "daily_new_infections": "New Inf.",
        "daily_recoveries": "New Rec.",
        "daily_deaths": "New Deaths",
        "total_population": "Total",
        "total_ever_infected": "Ever Inf.",
        "infected_percent": "Inf. %"
    })

    display_df = display_df[
        [
            "Day",
            "Healthy",
            "Infected",
            "Recovered",
            "Dead",
            "New Inf.",
            "New Rec.",
            "New Deaths",
            "Total",
            "Ever Inf.",
            "Inf. %"
        ]
    ]

    display_df["Inf. %"] = display_df["Inf. %"].round(2)

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )

    csv = results_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Live Visual Simulation Results CSV",
        data=csv,
        file_name="live_visual_simulation_results.csv",
        mime="text/csv"
    )

else:
    st.info("Set the parameters and click 'Generate Live Visual Simulation'.")
