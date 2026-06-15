import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

DATA_FILE = Path("data/processed/tb_cleaned.csv")
MODELS_DIR = Path("models")
OUTPUT_RESULTS = MODELS_DIR / "model_results.csv"

MODELS_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_FILE)

# Remove World, continents, and income groups
df = df[~df["code"].astype(str).str.startswith("OWID")]

df = df[["country", "year", "tb_incidence_per_100k", "tb_cases"]]
df = df.dropna()

# Encode country as a number
label_encoder = LabelEncoder()
df["country_encoded"] = label_encoder.fit_transform(df["country"])

# Features and target
X = df[["country_encoded", "year", "tb_incidence_per_100k"]]
y = df["tb_cases"]

# 70% training and 30% testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)

# Tuned models to avoid overfitting and keep accuracy more realistic
models = {
    "Linear Regression": LinearRegression(),

    "Decision Tree": DecisionTreeRegressor(
        max_depth=4,
        min_samples_leaf=25,
        random_state=42
    ),

    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        max_depth=6,
        min_samples_leaf=10,
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

joblib.dump(label_encoder, MODELS_DIR / "country_label_encoder.pkl")
joblib.dump(X.columns.tolist(), MODELS_DIR / "feature_columns.pkl")

results_df = pd.DataFrame(results)
results_df.to_csv(OUTPUT_RESULTS, index=False)

print("\nModel training completed successfully!")
print("\nModel Results:")
print(results_df)

best_model = results_df.sort_values(by="R2 Score", ascending=False).iloc[0]

print("\nBest Model:")
print(best_model)
