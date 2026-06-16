import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Dataset Analysis",
    layout="wide"
)

st.title("Dataset Analysis")

st.markdown("""
This page shows the cleaned TB dataset and allows the user to analyse TB cases by country.
When a country is selected, both the chart and the table update for that selected country.
""")

DATA_FILE = Path("data/processed/tb_cleaned.csv")

df = pd.read_csv(DATA_FILE)

# Remove World, continents, and income groups
df = df[~df["code"].astype(str).str.startswith("OWID")]

df = df.dropna()
df = df.sort_values(["country", "year"])

st.subheader("Dataset Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(df))
col2.metric("Total Countries", df["country"].nunique())
col3.metric("Start Year", int(df["year"].min()))
col4.metric("End Year", int(df["year"].max()))

st.subheader("Interactive Country Trend")

countries = sorted(df["country"].dropna().unique())

selected_country = st.selectbox(
    "Select a country",
    countries,
    index=countries.index("Pakistan") if "Pakistan" in countries else 0
)

country_data = df[df["country"] == selected_country].copy()
country_data = country_data.sort_values("year")

fig = px.line(
    country_data,
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

st.subheader(f"Selected Country Data: {selected_country}")

display_df = country_data.rename(columns={
    "country": "Country",
    "code": "Code",
    "year": "Year",
    "tb_cases": "TB Cases",
    "tb_incidence_per_100k": "TB Incidence per 100k"
})

display_df = display_df[
    [
        "Country",
        "Code",
        "Year",
        "TB Cases",
        "TB Incidence per 100k"
    ]
]

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)

st.subheader("Top 10 Countries by Latest TB Cases")

latest_year = df["year"].max()
latest_df = df[df["year"] == latest_year].copy()

top_cases = latest_df.sort_values("tb_cases", ascending=False).head(10)

fig2 = px.bar(
    top_cases,
    x="country",
    y="tb_cases",
    title=f"Top 10 Countries by TB Cases in {latest_year}"
)

fig2.update_layout(
    xaxis_title="Country",
    yaxis_title="TB Cases"
)

st.plotly_chart(fig2, width="stretch")

st.subheader("Top 10 Countries by Latest TB Incidence")

top_incidence = latest_df.sort_values("tb_incidence_per_100k", ascending=False).head(10)

fig3 = px.bar(
    top_incidence,
    x="country",
    y="tb_incidence_per_100k",
    title=f"Top 10 Countries by TB Incidence per 100k in {latest_year}"
)

fig3.update_layout(
    xaxis_title="Country",
    yaxis_title="TB Incidence per 100k"
)

st.plotly_chart(fig3, width="stretch")
