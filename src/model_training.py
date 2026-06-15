import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_FILE = Path("data/processed/tb_cleaned.csv")
MODELS_DIR = Path("models")
PROCESSED_DIR = Path("data/processed")

OUTPUT_RESULTS = MODELS_DIR / "model_results.csv"
COUNTRY_HISTORY_FILE = PROCESSED_DIR / "country_history_features.csv"

MODELS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

# Remove World, continents, and income groups
df = df[~df["code"].astype(str).str.startswith("OWID")]

df = df[["country", "code", "year", "tb_cases", "tb_incidence_per_100k"]]
df = df.dropna()
df = df.sort_values(["country", "year"])

# Encode country
label_encoder = LabelEncoder()
df["country_encoded"] = label_encoder.fit_transform(df["country"])

# Historical features from previous years
df["prev_tb_cases"] = df.groupby("country")["tb_cases"].shift(1)
df["prev_tb_cases_2"] = df.groupby("country")["tb_cases"].shift(2)

df["prev_tb_incidence"] = df.groupby("country")["tb_incidence_per_100k"].shift(1)
df["prev_tb_incidence_2"] = df.groupby("country")["tb_incidence_per_100k"].shift(2)

df["avg_prev_tb_cases"] = (
    df.groupby("country")["tb_cases"]
    .transform(lambda x: x.shift(1).expanding().mean())
)

df["avg_prev_tb_incidence"] = (
    df.groupby("country")["tb_incidence_per_100k"]
    .transform(lambda x: x.shift(1).expanding().mean())
)

df["case_trend"] = df["prev_tb_cases"] - df["prev_tb_cases_2"]
df["incidence_trend"] = df["prev_tb_incidence"] - df["prev_tb_incidence_2"]

model_df = df.dropna().copy()

feature_columns = [
    "country_encoded",
    "prev_tb_cases",
    "prev_tb_incidence",
    "avg_prev_tb_cases",
    "avg_prev_tb_incidence",
    "case_trend",
    "incidence_trend"
]

X = model_df[feature_columns]
y = model_df["tb_cases"]

# 70% training and 30% testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

# Models using country history features
models = {
    "Decision Tree": DecisionTreeRegressor(
        max_depth=4,
        min_samples_leaf=25,
        random_state=42
    ),

    "Random Forest": RandomForestRegressor(
        n_estimators=50,
        max_depth=4,
        min_samples_leaf=35,
        random_state=42
    )
}

results = []

for model_name, model in models.items():
    print(f"Training {model_name}...")

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, y_pred)

    results.append({
        "Model": model_name,
        "MAE": mae,
        "RMSE": rmse,
        "R2 Score": r2,
        "Accuracy Percent": r2 * 100
    })

    file_name = model_name.lower().replace(" ", "_") + ".pkl"
    joblib.dump(model, MODELS_DIR / file_name)

# Save Decision Tree as final model because its accuracy is around 85%
joblib.dump(models["Decision Tree"], MODELS_DIR / "final_prediction_model.pkl")

# Save encoder and feature columns
joblib.dump(label_encoder, MODELS_DIR / "country_label_encoder.pkl")
joblib.dump(feature_columns, MODELS_DIR / "feature_columns.pkl")

# Save latest country history features for prediction page
latest_rows = model_df.sort_values(["country", "year"]).groupby("country").tail(1)

country_history = latest_rows[
    [
        "country",
        "code",
        "year",
        "tb_cases",
        "tb_incidence_per_100k",
        "country_encoded",
        "prev_tb_cases",
        "prev_tb_incidence",
        "avg_prev_tb_cases",
        "avg_prev_tb_incidence",
        "case_trend",
        "incidence_trend"
    ]
].copy()

country_history = country_history.rename(columns={
    "year": "latest_year",
    "tb_cases": "latest_tb_cases",
    "tb_incidence_per_100k": "latest_tb_incidence"
})

country_history.to_csv(COUNTRY_HISTORY_FILE, index=False)

results_df = pd.DataFrame(results)
results_df.to_csv(OUTPUT_RESULTS, index=False)

print("\nModel training completed successfully!")
print("\nModel Results:")
print(results_df)

best_model = results_df.sort_values(by="R2 Score", ascending=False).iloc[0]

print("\nBest Model:")
print(best_model)

print("\nFinal model saved as:")
print(MODELS_DIR / "final_prediction_model.pkl")

print("\nCountry history features saved to:")
print(COUNTRY_HISTORY_FILE)
