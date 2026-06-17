import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys
from styles import apply_custom_style, page_header

sys.path.append(str(Path("src").resolve()))

from prediction import predict_tb_cases

st.set_page_config(
    page_title="ML Prediction",
    page_icon="🤖",
    layout="wide"
)

apply_custom_style()

page_header(
    title="TB Case Prediction",
    subtitle="Predict expected TB cases for 2026 using country history or a custom TB incidence value.",
    badge="Machine Learning Prediction"
)
st.info(
    "Automatic mode uses the selected country's recent TB history. "
    "Custom mode allows the user to test a different TB incidence value."
)

DATA_FILE = Path("data/processed/tb_cleaned.csv")
HISTORY_FILE = Path("data/processed/country_history_features.csv")

df = pd.read_csv(DATA_FILE)
history_df = pd.read_csv(HISTORY_FILE)

# Remove World, continents, and income groups
df = df[~df["code"].astype(str).str.startswith("OWID")]

countries = sorted(history_df["country"].dropna().unique())

st.subheader("Prediction Inputs")

col1, col2 = st.columns(2)

with col1:
    selected_country = st.selectbox("Select Country", countries)

country_history_row = history_df[history_df["country"] == selected_country].iloc[0]
latest_incidence = float(country_history_row["latest_tb_incidence"])

with col2:
    prediction_mode = st.radio(
        "Prediction Mode",
        [
            "Automatic prediction from country history",
            "Custom prediction using TB incidence"
        ]
    )

custom_incidence = None

if prediction_mode == "Custom prediction using TB incidence":
    custom_incidence = st.number_input(
        "Enter TB incidence per 100k",
        min_value=0.0,
        max_value=1000.0,
        value=round(latest_incidence, 2),
        step=1.0
    )
else:
    st.info(
        f"Automatic mode will use the latest historical TB incidence for "
        f"{selected_country}: {latest_incidence:.2f} per 100k."
    )

if st.button("Predict TB Cases for 2026"):

    if prediction_mode == "Automatic prediction from country history":
        result = predict_tb_cases(selected_country)
    else:
        result = predict_tb_cases(selected_country, custom_incidence)

    st.subheader("Prediction Result")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Country", result["country"])
    m2.metric("Prediction Year", "2026")
    m3.metric("Predicted TB Cases", f"{result['predicted_cases_2026']:,.0f}")
    m4.metric("Risk Level", result["risk_level"])

    st.markdown("### How this prediction was made")

    if result["prediction_type"] == "Automatic history-based prediction":
        st.success(
            "The system used the selected country's previous TB history, "
            "latest TB cases, latest TB incidence, and trend values to predict 2026 TB cases."
        )
    else:
        st.success(
            "The system used the selected country's previous TB history, "
            "but replaced the latest incidence value with your custom TB incidence value."
        )

    st.subheader("Country Historical Information Used")

    info_col1, info_col2, info_col3, info_col4 = st.columns(4)

    info_col1.metric("Latest Dataset Year", result["latest_year"])
    info_col2.metric("Latest TB Cases", f"{result['latest_tb_cases']:,.0f}")
    info_col3.metric("Latest TB Incidence", f"{result['latest_tb_incidence']:.2f}")
    info_col4.metric("Used TB Incidence", f"{result['selected_incidence']:.2f}")

    st.subheader("Recent TB Data for Selected Country")

    country_df = df[df["country"] == selected_country].sort_values("year")
    recent_df = country_df.tail(10).copy()

    recent_display = recent_df.rename(columns={
        "year": "Year",
        "tb_cases": "TB Cases",
        "tb_incidence_per_100k": "TB Incidence per 100k"
    })

    recent_display = recent_display[
        [
            "Year",
            "TB Cases",
            "TB Incidence per 100k"
        ]
    ]

    st.dataframe(
        recent_display,
        width="stretch",
        hide_index=True
    )

    st.subheader("Country TB Cases Trend")

    fig = px.line(
        country_df,
        x="year",
        y="tb_cases",
        markers=True,
        title=f"TB Cases Trend in {selected_country}"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="TB Cases"
    )

    st.plotly_chart(fig, width="stretch")

else:
    st.info("Select a country and prediction mode, then click the prediction button.")
