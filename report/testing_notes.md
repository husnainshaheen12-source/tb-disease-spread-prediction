# Testing Notes

## 1. Data Cleaning Test

Command used:
python src/data_cleaning.py

Expected result:
- Raw TB datasets are loaded.
- Columns are renamed.
- Missing values are removed.
- Cleaned dataset is saved as data/processed/tb_cleaned.csv.

## 2. Data Analysis Test

Command used:
python src/data_analysis.py

Expected result:
- Country-only dataset is created.
- Non-country records are removed.
- Analysis charts are saved in the report folder.

## 3. Model Training Test

Command used:
python src/model_training.py

Expected result:
- Linear Regression model is trained.
- Decision Tree model is trained.
- Random Forest model is trained.
- Model results are saved.
- Best model is selected based on R2 score.

## 4. Prediction Test

Example input:
- Country: Pakistan
- Year: 2026
- TB incidence per 100k: 250

Expected result:
- Predicted TB cases are displayed.
- Risk level is displayed.

## 5. Standard Simulation Test

Command used:
python src/simulation.py

Expected result:
- Simulation CSV is created.
- Simulation chart is created.

## 6. Streamlit Dashboard Test

Command used:
streamlit run streamlit_app/app.py

Expected result:
Dashboard opens with these pages:
1. Home
2. Dataset Analysis
3. ML Prediction
4. Simulation
5. Live Visual Simulation

## 7. Live Visual Simulation Test

Expected result:
- Green circles show healthy people.
- Red circles show infected people.
- Blue circles show recovered people.
- Gray circles show dead people.
- Alerts appear when infections increase.
- Mask and lockdown policy messages are displayed.
