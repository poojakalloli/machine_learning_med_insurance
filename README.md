# 🏥 Medical Insurance Charge Prediction System

An end-to-end Machine Learning application that predicts estimated annual medical insurance charges based on customer demographic and lifestyle information.

The project combines **Python, Pandas, NumPy, Scikit-learn, FastAPI, and Streamlit** to provide an interactive insurance premium prediction system.

---

## 📌 Project Overview

The goal of this project is to build a Machine Learning regression system capable of estimating medical insurance charges using customer information such as:

- Age
- Sex
- BMI
- Number of children
- Smoking status
- Region

The trained Machine Learning pipeline is integrated into an interactive Streamlit application for real-time predictions.

The application also provides:

- Customer Profile
- BMI Category
- What-If Analysis
- Premium Comparison
- Prediction History
- CSV Export
- Interactive prediction summary

---

## 🎯 Objectives

- Perform Exploratory Data Analysis (EDA)
- Understand relationships between customer attributes and insurance charges
- Preprocess numerical and categorical features
- Apply feature engineering
- Train multiple Machine Learning regression models
- Compare model performance
- Build a reusable Scikit-learn Pipeline
- Save the trained model using Joblib
- Build an API using FastAPI
- Build an interactive UI using Streamlit
- Deploy the prediction application using Streamlit

---

## 📊 Dataset

The project uses a medical insurance dataset containing customer demographic and lifestyle information.

### Main Features

| Feature | Description |
|---|---|
| `age` | Customer age |
| `sex` | Customer gender |
| `bmi` | Body Mass Index |
| `children` | Number of dependent children |
| `smoker` | Smoking status |
| `region` | Customer residential region |
| `charges` | Annual medical insurance charge |

### Target Variable

The original target is:

```text
charges
