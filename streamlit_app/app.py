import streamlit as st
from styles import apply_custom_style, page_header

st.set_page_config(
    page_title="TB Spread Prediction System",
    page_icon="🫁",
    layout="wide"
)

apply_custom_style()

page_header(
    title="AI-Based Tuberculosis Spread Simulation and TB Case Prediction System",
    subtitle="An interactive data science project that analyses real TB data, predicts future TB cases, and simulates how TB may spread in a population.",
    badge="Final Year Data Science Project"
)

st.markdown("## Project Overview")

st.markdown("""
Tuberculosis, also known as **TB**, is a bacterial infectious disease that mainly spreads through the air when an infected person coughs, sneezes, or stays in close contact with other people.

This project combines **data analysis**, **machine learning**, and **simulation** to understand TB trends and support disease spread awareness.
""")

st.markdown("## Main Features")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="card-icon">📊</div>
            <div class="card-title">Dataset Analysis</div>
            <div class="card-text">
                Shows country-level TB records, summary statistics, generated charts, and selected country trends.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="card-icon">🤖</div>
            <div class="card-title">ML Prediction</div>
            <div class="card-text">
                Predicts expected TB cases for 2026 using country history and optional TB incidence input.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="card-icon">📈</div>
            <div class="card-title">Spread Simulation</div>
            <div class="card-text">
                Simulates TB spread day by day using infection, recovery, death, mask, lockdown, and crowding factors.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="card-icon">🟢</div>
            <div class="card-title">Live Visualisation</div>
            <div class="card-text">
                Shows TB spread using moving dots: healthy, infected, recovered, and dead people.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("## Project Objectives")

obj1, obj2 = st.columns(2)

with obj1:
    st.markdown("""
    - Analyse real-world TB data.
    - Understand TB trends by country and year.
    - Clean and prepare the dataset for analysis.
    - Show useful charts and summaries.
    """)

with obj2:
    st.markdown("""
    - Train and test prediction models.
    - Predict expected TB cases for 2026.
    - Simulate disease spread in a population.
    - Build a complete interactive Streamlit dashboard.
    """)

st.markdown("## How to Use This App")

st.info(
    "Use the sidebar on the left to open Dataset Analysis, ML Prediction, Simulation, and Live Visual Simulation pages."
)