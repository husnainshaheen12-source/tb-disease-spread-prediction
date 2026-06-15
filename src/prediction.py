import pandas as pd
import joblib
from pathlib import Path

MODEL_FILE = Path("models/final_prediction_model.pkl")
FEATURE_COLUMNS_FILE = Path("models/feature_columns.pkl")
COUNTRY_HISTORY_FILE = Path("data/processed/country_history_features.csv")

model = joblib.load(MODEL_FILE)
feature_columns = joblib.load(FEATURE_COLUMNS_FILE)
country_history_df = pd.read_csv(COUNTRY_HISTORY_FILE)


def get_risk_level(incidence):
    if incidence < 50:
        return "Low Risk"
    elif incidence < 150:
        return "Medium Risk"
    else:
        return "High Risk"


def predict_tb_cases(country, custom_incidence=None):
    country_row = country_history_df[
        country_history_df["country"].str.lower() == country.lower()
    ]

    if country_row.empty:
        raise ValueError("Country not found in the historical dataset.")

    row = country_row.iloc[0]

    if custom_incidence is None:
        selected_incidence = float(row["latest_tb_incidence"])
        prediction_type = "Automatic history-based prediction"
    else:
        selected_incidence = float(custom_incidence)
        prediction_type = "Custom incidence prediction"

    input_data = {
        "country_encoded": float(row["country_encoded"]),
        "prev_tb_cases": float(row["latest_tb_cases"]),
        "prev_tb_incidence": selected_incidence,
        "avg_prev_tb_cases": float(row["avg_prev_tb_cases"]),
        "avg_prev_tb_incidence": float(row["avg_prev_tb_incidence"]),
        "case_trend": float(row["latest_tb_cases"]) - float(row["prev_tb_cases"]),
        "incidence_trend": selected_incidence - float(row["prev_tb_incidence"])
    }

    input_df = pd.DataFrame([input_data])
    input_df = input_df[feature_columns]

    predicted_cases = model.predict(input_df)[0]
    predicted_cases = max(0, predicted_cases)

    return {
        "country": country,
        "prediction_type": prediction_type,
        "latest_year": int(row["latest_year"]),
        "latest_tb_cases": float(row["latest_tb_cases"]),
        "latest_tb_incidence": float(row["latest_tb_incidence"]),
        "selected_incidence": selected_incidence,
        "predicted_cases_2026": float(predicted_cases),
        "risk_level": get_risk_level(selected_incidence)
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
    print(f"Predicted TB Cases for 2026: {result['predicted_cases_2026']:.2f}")
    print(f"Risk Level: {result['risk_level']}")
