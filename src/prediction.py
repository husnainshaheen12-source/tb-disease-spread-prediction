import pandas as pd
import numpy as np
from pathlib import Path

COUNTRY_DATA_FILE = Path("data/processed/tb_country_only.csv")

if not COUNTRY_DATA_FILE.exists():
    COUNTRY_DATA_FILE = Path("data/processed/tb_cleaned.csv")

df = pd.read_csv(COUNTRY_DATA_FILE)

# Remove World, continents, and income groups
if "code" in df.columns:
    df = df[~df["code"].astype(str).str.startswith("OWID")]

df = df.dropna()
df = df.sort_values(["country", "year"])


def get_risk_level(incidence):
    if incidence < 50:
        return "Low Risk"
    elif incidence < 150:
        return "Medium Risk"
    else:
        return "High Risk"


def predict_from_country_history(country_df, target_year=2026):
    country_df = country_df.sort_values("year").copy()

    latest_row = country_df.iloc[-1]

    latest_year = int(latest_row["year"])
    latest_cases = float(latest_row["tb_cases"])
    latest_incidence = float(latest_row["tb_incidence_per_100k"])

    recent_df = country_df.tail(5)

    if len(recent_df) >= 2:
        years = recent_df["year"].astype(float).to_numpy()
        cases = recent_df["tb_cases"].astype(float).to_numpy()

        # Recent country trend using last few years
        slope = np.polyfit(years, cases, 1)[0]
    else:
        slope = 0

    years_forward = max(0, target_year - latest_year)

    predicted_cases = latest_cases + (slope * years_forward)

    # Safety limit so prediction does not jump unrealistically
    max_allowed_change = max(10, latest_cases * 0.40)

    lower_limit = max(0, latest_cases - max_allowed_change)
    upper_limit = latest_cases + max_allowed_change

    predicted_cases = min(max(predicted_cases, lower_limit), upper_limit)

    return predicted_cases, latest_year, latest_cases, latest_incidence, slope


def predict_tb_cases(country, custom_incidence=None):
    country_row = df[df["country"].str.lower() == country.lower()]

    if country_row.empty:
        raise ValueError("Country not found in the historical dataset.")

    actual_country_name = country_row.iloc[0]["country"]

    (
        history_prediction,
        latest_year,
        latest_tb_cases,
        latest_tb_incidence,
        recent_trend
    ) = predict_from_country_history(country_row)

    if custom_incidence is None:
        selected_incidence = latest_tb_incidence
        predicted_cases = history_prediction
        prediction_type = "Automatic history-based prediction"
    else:
        selected_incidence = float(custom_incidence)
        prediction_type = "Custom incidence prediction"

        if latest_tb_incidence > 0:
            incidence_ratio = selected_incidence / latest_tb_incidence
        else:
            incidence_ratio = 1

        # Avoid unrealistic extreme values
        incidence_ratio = min(max(incidence_ratio, 0), 5)

        predicted_cases = history_prediction * incidence_ratio

    predicted_cases = max(0, predicted_cases)

    return {
        "country": actual_country_name,
        "prediction_type": prediction_type,
        "latest_year": latest_year,
        "latest_tb_cases": latest_tb_cases,
        "latest_tb_incidence": latest_tb_incidence,
        "selected_incidence": selected_incidence,
        "predicted_cases_2026": predicted_cases,
        "risk_level": get_risk_level(selected_incidence),
        "recent_trend": recent_trend
    }


if __name__ == "__main__":
    print("TB Case Prediction System")
    print("-------------------------")

    country = input("Enter country name: ")

    incidence_input = input(
        "Enter TB incidence per 100k, or press Enter for automatic history-based prediction: "
    )

    if incidence_input.strip() == "":
        result = predict_tb_cases(country)
    else:
        result = predict_tb_cases(country, float(incidence_input))

    print("\nPrediction Result")
    print("-----------------")
    print(f"Country: {result['country']}")
    print(f"Prediction Type: {result['prediction_type']}")
    print(f"Latest Dataset Year: {result['latest_year']}")
    print(f"Latest TB Cases: {result['latest_tb_cases']:.0f}")
    print(f"Latest TB Incidence per 100k: {result['latest_tb_incidence']:.2f}")
    print(f"Used TB Incidence per 100k: {result['selected_incidence']:.2f}")
    print(f"Recent yearly trend: {result['recent_trend']:.2f}")
    print(f"Predicted TB Cases for 2026: {result['predicted_cases_2026']:.2f}")
    print(f"Risk Level: {result['risk_level']}")
