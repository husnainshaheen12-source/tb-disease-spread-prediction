# AI-Based Tuberculosis Spread Simulation and TB Case Prediction System

## 1. Introduction

Tuberculosis, also known as TB, is a bacterial infectious disease that mainly affects the lungs. It spreads through the air when an infected person coughs, sneezes, or stays in close contact with other people.

This project presents an AI-based Tuberculosis Spread Simulation and TB Case Prediction System. The system uses real-world TB data, machine learning models, and simulation techniques to analyse TB trends, predict estimated TB cases, and visually demonstrate how infection can spread in a population.

## 2. Project Objectives

The main objectives of this project are:

1. To collect and clean tuberculosis dataset records.
2. To analyse TB cases and incidence trends by country and year.
3. To train machine learning models for TB case prediction.
4. To create a disease spread simulation.
5. To build an interactive Streamlit dashboard.
6. To show live visual infection spread using moving circles.
7. To display policy alerts for masks, lockdown, treatment, and isolation.

## 3. Dataset Description

The dataset contains country-level tuberculosis data. Important columns include:

- Country
- Country code
- Year
- Estimated TB cases
- TB incidence per 100,000 population

The data was cleaned and processed using Python. Non-country records such as World, Asia, Africa, and income groups were removed to make the analysis more accurate.

## 4. Dataset Analysis

The dataset analysis includes:

- Global TB cases trend over time
- Top 10 countries by TB cases
- Top 10 countries by TB incidence
- Pakistan TB cases trend
- Country-level interactive trend analysis

## 5. Machine Learning Models

Three machine learning models were trained:

1. Linear Regression
2. Decision Tree Regressor
3. Random Forest Regressor

The target variable was estimated TB cases. The input features included country, year, and TB incidence per 100,000 population.

The Random Forest model performed the best and was used in the Streamlit dashboard for prediction.

## 6. Simulation

The project includes a standard TB spread simulation. The simulation tracks:

- Healthy people
- Infected people
- Recovered people

The simulation includes factors such as infection rate, recovery rate, mask effect, lockdown effect, and hospital crowd effect.

## 7. Live Visual Simulation

The live visual simulation shows each person as a moving circle.

Circle colours:

- Green = Healthy
- Red = Infected
- Blue = Recovered
- Gray = Dead

The live simulation also includes policy alerts. When infection increases, the system displays alerts such as masks are compulsory, lockdown is compulsory, and isolation/treatment is required.

## 8. Streamlit Dashboard

The dashboard contains the following pages:

1. Home Page
2. Dataset Analysis
3. ML Prediction
4. Simulation
5. Live Visual Simulation

## 9. Results

The project successfully created:

- A cleaned TB dataset
- Data analysis charts
- Machine learning prediction models
- Standard disease spread simulation
- Live visual simulation
- Streamlit dashboard
- Policy alert system

## 10. Conclusion

This project demonstrates how data science, machine learning, and simulation can be used to study tuberculosis spread. The system helps users understand TB trends, predict estimated TB cases, and observe how interventions such as masks, lockdown, and treatment can affect disease spread.
