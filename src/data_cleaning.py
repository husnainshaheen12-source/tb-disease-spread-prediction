import pandas as pd
from pathlib import Path

# File paths
RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")

cases_file = RAW_DATA_DIR / "tb_cases.csv"
incidence_file = RAW_DATA_DIR / "tb_incidence.csv"
output_file = PROCESSED_DATA_DIR / "tb_cleaned.csv"

# Create processed folder if it does not exist
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Load datasets
cases_df = pd.read_csv(cases_file)
incidence_df = pd.read_csv(incidence_file)

print("TB Cases Dataset Columns:")
print(cases_df.columns)

print("\nTB Incidence Dataset Columns:")
print(incidence_df.columns)

# Rename common columns
cases_df = cases_df.rename(columns={
    "Entity": "country",
    "Code": "code",
    "Year": "year"
})

incidence_df = incidence_df.rename(columns={
    "Entity": "country",
    "Code": "code",
    "Year": "year"
})

# Automatically find value columns
cases_value_column = [col for col in cases_df.columns if col not in ["country", "code", "year"]][0]
incidence_value_column = [col for col in incidence_df.columns if col not in ["country", "code", "year"]][0]

cases_df = cases_df.rename(columns={
    cases_value_column: "tb_cases"
})

incidence_df = incidence_df.rename(columns={
    incidence_value_column: "tb_incidence_per_100k"
})

# Merge datasets
df = pd.merge(
    cases_df,
    incidence_df,
    on=["country", "code", "year"],
    how="inner"
)

# Clean data
df = df.dropna()
df = df[df["tb_cases"] >= 0]
df = df[df["tb_incidence_per_100k"] >= 0]

# Convert columns
df["year"] = df["year"].astype(int)
df["tb_cases"] = df["tb_cases"].astype(float)
df["tb_incidence_per_100k"] = df["tb_incidence_per_100k"].astype(float)

# Save cleaned dataset
df.to_csv(output_file, index=False)

print("\nCleaned dataset created successfully!")
print(f"Saved to: {output_file}")
print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)
