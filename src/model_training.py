import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# File paths
DATA_FILE = Path("data/processed/tb_cleaned.csv")
MODELS_DIR = Path("models")
OUTPUT_RESULTS = MODELS_DIR / "model_results.csv"

MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_FILE)

# Remove world/continent/income-group records and keep country-level data only
df = df[~df["code"].astype(str).str.startswith("OWID")]

# Select useful columns
df = df[["country", "year", "tb_incidence_per_100k", "tb_cases"]]

# Remove missing values
df = df.dropna()

# Features and target
X = df[["country", "year", "tb_incidence_per_100k"]]
y = df["tb_cases"]

# Convert country column into numeric dummy columns
X = pd.get_dummies(X, columns=["country"], drop_first=True)

# Save feature columns for future prediction
joblib.dump(X.columns.tolist(), MODELS_DIR / "feature_columns.pkl")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Define models
models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
}

results = []

# Train and evaluate each model
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
        "R2 Score": r2
    })
    
    # Save model
    file_name = model_name.lower().replace(" ", "_") + ".pkl"
    joblib.dump(model, MODELS_DIR / file_name)

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv(OUTPUT_RESULTS, index=False)

print("\nModel training completed successfully!")
print("\nModel Results:")
print(results_df)

# Show best model
best_model = results_df.sort_values(by="R2 Score", ascending=False).iloc[0]
print("\nBest Model:")
print(best_model)
