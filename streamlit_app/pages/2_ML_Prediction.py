import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add src folder to Python path
sys.path.append(str(Path("src").resolve()))

from prediction import predict_tb_cases, get_risk_level

st.set_page_config(
    page_title="ML Prediction",
    page_icon="ML",
    layout="wide"
)

st.title("TB Case Prediction Using Machine Learning")

st.markdown("""
This page uses the trained **Random Forest model** to predict estimated TB cases.
The prediction is based on:

- Country
- Year
- TB incidence per 100,000 population
""")

DATA_FILE = Path("data/processed/tb_country_only.csv")
MODEL_RESULTS_FILE = Path("models/model_results.csv")

if not DATA_FILE.exists():
    st.error("Country dataset not found. Please run src/data_analysis.py first.")
    st.stop()

df = pd.read_csv(DATA_FILE)

st.subheader("Model Performance")

if MODEL_RESULTS_FILE.exists():
    results_df = pd.read_csv(MODEL_RESULTS_FILE)
    st.dataframe(results_df, use_container_width=True)

    best_model = results_df.sort_values(by="R2 Score", ascending=False).iloc[0]
    st.success(f"Best Model: {best_model['Model']} with R2 Score: {best_model['R2 Score']:.4f}")
else:
    st.warning("Model results file not found.")

st.subheader("Enter Prediction Details")

countries = sorted(df["country"].unique())

default_index = countries.index("Pakistan") if "Pakistan" in countries else 0

col1, col2, col3 = st.columns(3)

with col1:
    country = st.selectbox("Select Country", countries, index=default_index)

with col2:
    year = st.number_input(
        "Enter Year",
        min_value=2000,
        max_value=2035,
        value=2026,
        step=1
    )

with col3:
    tb_incidence = st.number_input(
        "TB Incidence per 100k",
        min_value=0.0,
        max_value=1000.0,
        value=250.0,
        step=1.0
    )

if st.button("Predict TB Cases"):
    predicted_cases = predict_tb_cases(country, int(year), float(tb_incidence))
    risk_level = get_risk_level(float(tb_incidence))

    st.subheader("Prediction Result")

    result_col1, result_col2, result_col3 = st.columns(3)

    result_col1.metric("Country", country)
    result_col2.metric("Predicted TB Cases", f"{predicted_cases:,.0f}")
    result_col3.metric("Risk Level", risk_level)

    if risk_level == "High Risk":
        st.error("This country is classified as High Risk based on TB incidence.")
    elif risk_level == "Medium Risk":
        st.warning("This country is classified as Medium Risk based on TB incidence.")
    else:
        st.success("This country is classified as Low Risk based on TB incidence.")

st.subheader("Recent Data for Selected Country")

country_data = df[df["country"] == country].sort_values(by="year", ascending=False)
st.dataframe(country_data.head(10), use_container_width=True)
