import pandas as pd
import joblib
from pathlib import Path

MODELS_DIR = Path("models")
MODEL_FILE = MODELS_DIR / "random_forest.pkl"
FEATURE_COLUMNS_FILE = MODELS_DIR / "feature_columns.pkl"
ENCODER_FILE = MODELS_DIR / "country_label_encoder.pkl"

model = joblib.load(MODEL_FILE)
feature_columns = joblib.load(FEATURE_COLUMNS_FILE)
label_encoder = joblib.load(ENCODER_FILE)

def predict_tb_cases(country, year, tb_incidence_per_100k):
    """
    Predict estimated TB cases using trained Random Forest model.
    """

    if country in label_encoder.classes_:
        country_encoded = label_encoder.transform([country])[0]
    else:
        country_encoded = 0
        print(f"Warning: Country '{country}' was not found in training data. Using default encoding.")

    input_data = pd.DataFrame({
        "country_encoded": [country_encoded],
        "year": [year],
        "tb_incidence_per_100k": [tb_incidence_per_100k]
    })

    input_data = input_data[feature_columns]

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
