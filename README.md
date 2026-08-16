# 🏥 Medical Insurance Charge Prediction System

An end-to-end Machine Learning web application designed to estimate annual medical insurance charges based on demographic and lifestyle attributes. Built using **FastAPI** for the backend model serving and **Streamlit** for an interactive user interface.

---

## 📌 Project Overview
* **Objective:** Predict individual medical costs to assist insurance providers with risk assessment and pricing transparency.
* **Target Variable:** Log-transformed annual charges (`charges_log`).
* **Top Model:** Gradient Boosting Regressor ($R^2 \approx 0.85+$).
* **Key Risk Factors:** Smoking status (accounts for >50% model variance), Age, and Body Mass Index (BMI).

---

## 📁 Project Architecture

```text
INSURANCE-ML-PROJECT/
├── Backend/
│   └── main.py                  # FastAPI server script & API endpoints
├── Frontend/
│   └── app_ui.py                # Streamlit user interface
├── models/
│   └── insurance_model.pkl      # Trained Scikit-Learn pipeline
├── dataset/
│   └── insurance.csv            # Raw insurance dataset
├── notebook/
│   └── EDA_and_Training.ipynb   # Model training & analysis code
├── requirements.txt             # Project dependencies
└── README.md                    # Documentation