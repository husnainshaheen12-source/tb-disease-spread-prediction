import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Dataset Analysis",
    page_icon="??",
    layout="wide"
)

st.title("TB Dataset Analysis")

DATA_FILE = Path("data/processed/tb_country_only.csv")
SUMMARY_FILE = Path("report/dataset_analysis_summary.csv")

GLOBAL_TREND_IMG = Path("report/global_tb_cases_trend.png")
TOP_CASES_IMG = Path("report/top_10_countries_tb_cases.png")
TOP_INCIDENCE_IMG = Path("report/top_10_countries_tb_incidence.png")
PAKISTAN_TREND_IMG = Path("report/pakistan_tb_cases_trend.png")

if not DATA_FILE.exists():
    st.error("Country-level dataset not found. Please run src/data_analysis.py first.")
    st.stop()

df = pd.read_csv(DATA_FILE)

st.markdown("""
This page shows tuberculosis data analysis using country-level TB records.
The analysis includes global trends, top countries by TB cases, TB incidence,
and country-wise trend visualization.
""")

# Summary metrics
st.subheader("Dataset Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", df.shape[0])
col2.metric("Total Countries", df["country"].nunique())
col3.metric("Start Year", int(df["year"].min()))
col4.metric("End Year", int(df["year"].max()))

if SUMMARY_FILE.exists():
    st.subheader("Analysis Summary Table")
    summary_df = pd.read_csv(SUMMARY_FILE)
    st.dataframe(summary_df, use_container_width=True)

# Display generated charts
st.subheader("Generated Analysis Charts")

col_a, col_b = st.columns(2)

with col_a:
    if GLOBAL_TREND_IMG.exists():
        st.image(str(GLOBAL_TREND_IMG), caption="Global TB Cases Trend")

with col_b:
    if PAKISTAN_TREND_IMG.exists():
        st.image(str(PAKISTAN_TREND_IMG), caption="Pakistan TB Cases Trend")

col_c, col_d = st.columns(2)

with col_c:
    if TOP_CASES_IMG.exists():
        st.image(str(TOP_CASES_IMG), caption="Top 10 Countries by TB Cases")

with col_d:
    if TOP_INCIDENCE_IMG.exists():
        st.image(str(TOP_INCIDENCE_IMG), caption="Top 10 Countries by TB Incidence")

# Interactive country chart
st.subheader("Interactive Country Trend")

countries = sorted(df["country"].unique())
selected_country = st.selectbox("Select a country", countries, index=countries.index("Pakistan") if "Pakistan" in countries else 0)

country_data = df[df["country"] == selected_country]

fig = px.line(
    country_data,
    x="year",
    y="tb_cases",
    markers=True,
    title=f"TB Cases Trend in {selected_country}",
    labels={
        "year": "Year",
        "tb_cases": "TB Cases"
    }
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Preview of Dataset")
st.dataframe(df.head(20), use_container_width=True)
