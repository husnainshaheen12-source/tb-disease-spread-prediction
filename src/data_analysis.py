import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# File paths
DATA_FILE = Path("data/processed/tb_cleaned.csv")
PROCESSED_DIR = Path("data/processed")
REPORT_DIR = Path("report")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Load cleaned data
df = pd.read_csv(DATA_FILE)

# Remove World, continents, and income groups
country_df = df[~df["code"].astype(str).str.startswith("OWID")].copy()

# Save country-only dataset
country_output = PROCESSED_DIR / "tb_country_only.csv"
country_df.to_csv(country_output, index=False)

print("Country-only dataset created successfully!")
print(f"Saved to: {country_output}")
print("Rows and columns:", country_df.shape)
print("Total countries:", country_df["country"].nunique())
print("Year range:", country_df["year"].min(), "to", country_df["year"].max())

# Set chart style
sns.set(style="whitegrid")

# 1. Global country-level TB trend
global_trend = country_df.groupby("year")["tb_cases"].sum().reset_index()

plt.figure(figsize=(10, 5))
sns.lineplot(data=global_trend, x="year", y="tb_cases", marker="o")
plt.title("Global TB Cases Trend Using Country-Level Data")
plt.xlabel("Year")
plt.ylabel("Total TB Cases")
plt.tight_layout()
plt.savefig(REPORT_DIR / "global_tb_cases_trend.png")
plt.close()

# 2. Top 10 countries by latest TB cases
latest_year = country_df["year"].max()
latest_data = country_df[country_df["year"] == latest_year]

top_10_cases = latest_data.sort_values(by="tb_cases", ascending=False).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(data=top_10_cases, x="tb_cases", y="country")
plt.title(f"Top 10 Countries by TB Cases in {latest_year}")
plt.xlabel("TB Cases")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig(REPORT_DIR / "top_10_countries_tb_cases.png")
plt.close()

# 3. Top 10 countries by TB incidence
top_10_incidence = latest_data.sort_values(
    by="tb_incidence_per_100k",
    ascending=False
).head(10)

plt.figure(figsize=(12, 6))
sns.barplot(data=top_10_incidence, x="tb_incidence_per_100k", y="country")
plt.title(f"Top 10 Countries by TB Incidence per 100k in {latest_year}")
plt.xlabel("TB Incidence per 100k")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig(REPORT_DIR / "top_10_countries_tb_incidence.png")
plt.close()

# 4. Pakistan TB cases trend
pakistan_data = country_df[country_df["country"] == "Pakistan"]

plt.figure(figsize=(10, 5))
sns.lineplot(data=pakistan_data, x="year", y="tb_cases", marker="o")
plt.title("TB Cases Trend in Pakistan")
plt.xlabel("Year")
plt.ylabel("TB Cases")
plt.tight_layout()
plt.savefig(REPORT_DIR / "pakistan_tb_cases_trend.png")
plt.close()

# 5. Save summary table
summary = {
    "total_rows": [country_df.shape[0]],
    "total_countries": [country_df["country"].nunique()],
    "start_year": [country_df["year"].min()],
    "end_year": [country_df["year"].max()],
    "latest_year": [latest_year],
    "highest_tb_cases_country": [top_10_cases.iloc[0]["country"]],
    "highest_tb_cases": [top_10_cases.iloc[0]["tb_cases"]],
    "highest_incidence_country": [top_10_incidence.iloc[0]["country"]],
    "highest_incidence_per_100k": [top_10_incidence.iloc[0]["tb_incidence_per_100k"]]
}

summary_df = pd.DataFrame(summary)
summary_df.to_csv(REPORT_DIR / "dataset_analysis_summary.csv", index=False)

print("\nCharts created successfully in report folder:")
print("- global_tb_cases_trend.png")
print("- top_10_countries_tb_cases.png")
print("- top_10_countries_tb_incidence.png")
print("- pakistan_tb_cases_trend.png")
print("- dataset_analysis_summary.csv")
