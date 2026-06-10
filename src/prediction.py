import pandas as pd
import joblib
from pathlib import Path

# File paths
MODELS_DIR = Path("models")
MODEL_FILE = MODELS_DIR / "random_forest.pkl"
FEATURE_COLUMNS_FILE = MODELS_DIR / "feature_columns.pkl"

# Load trained model and feature columns
model = joblib.load(MODEL_FILE)
feature_columns = joblib.load(FEATURE_COLUMNS_FILE)

def predict_tb_cases(country, year, tb_incidence_per_100k):
    """
    Predict estimated TB cases using trained Random Forest model.
    """

    # Create one row with all feature columns set to 0
    input_data = pd.DataFrame(0, index=[0], columns=feature_columns)

    # Set numeric values
    input_data["year"] = year
    input_data["tb_incidence_per_100k"] = tb_incidence_per_100k

    # Set country dummy column if available
    country_column = "country_" + country

    if country_column in input_data.columns:
        input_data[country_column] = 1
    else:
        print(f"Warning: Country '{country}' was not found in training data. Prediction may be less accurate.")

    # Predict
    prediction = model.predict(input_data)[0]

    return round(prediction, 2)

def get_risk_level(tb_incidence_per_100k):
    """
    Classify TB risk level based on incidence rate.
    """

    if tb_incidence_per_100k < 50:
        return "Low Risk"
    elif tb_incidence_per_100k < 150:
        return "Medium Risk"
    else:
        return "High Risk"

if __name__ == "__main__":
    print("TB Case Prediction System")
    print("-------------------------")

    country = input("Enter country name: ")
    year = int(input("Enter year: "))
    tb_incidence = float(input("Enter TB incidence per 100k: "))

    predicted_cases = predict_tb_cases(country, year, tb_incidence)
    risk_level = get_risk_level(tb_incidence)

    print("\nPrediction Result")
    print("-----------------")
    print(f"Country: {country}")
    print(f"Year: {year}")
    print(f"TB Incidence per 100k: {tb_incidence}")
    print(f"Predicted TB Cases: {predicted_cases}")
    print(f"Risk Level: {risk_level}")
