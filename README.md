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
During model training, the target variable is log-transformed:

charges_log = np.log1p(charges)

During prediction, the result is converted back to the original insurance-charge scale using:

predicted_charge = np.expm1(log_prediction)
🔎 Exploratory Data Analysis (EDA)

Exploratory Data Analysis was performed to understand the dataset and identify important patterns and relationships.

EDA includes:
Dataset overview
Dataset shape
Data types
Missing-value analysis
Duplicate-value analysis
Descriptive statistics
Univariate analysis
Bivariate analysis
Distribution analysis
Outlier analysis
Correlation analysis
Age vs Insurance Charges
BMI vs Insurance Charges
Smoking Status vs Insurance Charges
Children vs Insurance Charges
Region-wise analysis

The complete EDA and model training process is available in:

notebook/EDA_and_Training.ipynb.ipynb
🧹 Data Preprocessing

The preprocessing workflow includes:

Data cleaning
Data type checking
Missing-value checking
Duplicate checking
Feature selection
Numerical feature preprocessing
Categorical feature encoding
Target transformation
Train-test splitting
Machine Learning Pipeline creation

The preprocessing steps are combined with the Machine Learning model inside a reusable Scikit-learn Pipeline.

⚙️ Feature Engineering

BMI values are categorized to make the prediction results easier to understand.

BMI Categories
BMI Range	Category
Below 18.5	Underweight
18.5 – 24.9	Normal Weight
25.0 – 29.9	Overweight
30.0 and above	Obese

Example:

BMI: 28.5
Category: Overweight
🔄 Target Transformation

Insurance charges can have a skewed distribution.

The target variable was transformed during training using:

df["charges_log"] = np.log1p(df["charges"])

The model is trained using the transformed target.

During prediction, the output is converted back:

predicted_charge = np.expm1(log_prediction)

This allows the application to display the estimated premium in the original insurance-charge scale.

✂️ Train-Test Split

The dataset was divided into:

Training data
Testing data

The training data was used to train the Machine Learning models.

The testing data was used to evaluate model performance on unseen data.

🤖 Machine Learning Models

Multiple regression algorithms were explored and compared.

Models Used
Linear Regression
Ridge Regression
Lasso Regression
K-Nearest Neighbors Regressor
Support Vector Regressor
Decision Tree Regressor
Random Forest Regressor
Gradient Boosting Regressor
📈 Model Evaluation

The regression models were evaluated using:

Mean Absolute Error (MAE)
Mean Squared Error (MSE)
Root Mean Squared Error (RMSE)
R² Score

These metrics were used to compare model performance and select the final model.

🏆 Final Model

The trained Machine Learning pipeline is saved using Joblib:

models/insurance_model.pkl

The saved pipeline contains the preprocessing and prediction workflow required to generate insurance-charge predictions.

🔗 Machine Learning Pipeline

The project uses a Scikit-learn Pipeline to combine preprocessing and Machine Learning prediction.

The trained pipeline is saved using Joblib:

model = joblib.load(MODEL_PATH)

New customer information is passed to the pipeline:

prediction = model.predict(input_data)

The prediction is then converted back from the log scale using:

np.expm1()
🏗️ Project Architecture
                    ┌───────────────────────┐
                    │        User           │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │     Streamlit UI      │
                    │                       │
                    │ Customer Information  │
                    │ BMI Analysis          │
                    │ What-If Analysis      │
                    │ Prediction History    │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   ML Pipeline         │
                    │ insurance_model.pkl   │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Model Prediction    │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Inverse Transformation│
                    │       expm1()         │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │ Estimated Premium     │
                    │      INR / USD        │
                    └───────────────────────┘
🚀 Application Features
💰 1. Real-Time Premium Prediction

Users can enter:

Age
Sex
BMI
Number of Children
Smoker Status
Region

The application predicts the estimated annual insurance premium.

📊 2. BMI Analysis

The application automatically displays BMI and BMI category.

Example:

BMI: 28.5
Category: Overweight
👤 3. Customer Profile

The application provides a professional customer profile containing:

Age
BMI
BMI Category
Smoking Status
Region
Gender
Number of Children

Example:

AGE       : 35 years
BMI       : 28.5
CATEGORY  : Overweight
SMOKER    : Yes
REGION    : Southeast

Profile:

Male • 0 children • BMI 28.5 • Overweight
🔄 4. What-If Analysis

The What-If Analysis allows users to change customer details and compare the new estimated premium with the current prediction.

Example:

Current Smoker:
Yes


What-If Smoker:
No

The application displays:

Current Premium
What-If Premium
Premium Difference
USD Difference
Changed Customer Details

Example:

CURRENT PREMIUM
₹1,583,353.52


WHAT-IF PREMIUM
₹419,109.82


PREMIUM DIFFERENCE
₹1,164,243.69

Users can also save the What-If result to prediction history.

📜 5. Prediction History

The application maintains prediction history during the current Streamlit session.

It displays:

Total Predictions
Latest Premium
Average Premium
Prediction Timestamp
Prediction Number
Customer Profile
BMI
BMI Category
Smoking Status
Region
Premium in INR
Premium in USD
📥 6. Export History

Users can export prediction history as a CSV file.

The exported data contains:

Time
Prediction Type
Age
Sex
BMI
BMI Category
Children
Smoker
Region
Premium (INR)
Premium (USD)
🔌 FastAPI Backend

The project includes a FastAPI backend for API-based model serving.

Backend file:

Backend/main.py
API Endpoints

Health Check:

GET /

Prediction:

POST /predict
Swagger Documentation
Run the backend locally:

uvicorn Backend.main:app --reload

Then open:

http://127.0.0.1:8000/docs

FastAPI provides interactive API documentation through Swagger UI.

🖥️ Streamlit Frontend

The Streamlit application is located at:

Frontend/app_ui.py

The application directly loads the trained Machine Learning pipeline.

Run the application using:

streamlit run Frontend/app_ui.py

The application will be available at:

http://localhost:8501
📁 Project Structure
INSURANCE-ML-PROJECT/
│
├── Backend/
│   └── main.py
│
├── Frontend/
│   ├── app_ui.py
│   └── app_ui_backup.py
│
├── dataset/
│   └── insurance.csv
│
├── models/
│   └── insurance_model.pkl
│
├── notebook/
│   └── EDA_and_Training.ipynb.ipynb
│
├── requirements.txt
├── README.md
└── .gitignore
🛠️ Technologies Used
Programming Language
Python
Data Analysis
Pandas
NumPy
Data Visualization
Matplotlib
Seaborn
Machine Learning
Scikit-learn
Joblib
Backend
FastAPI
Uvicorn
Frontend
Streamlit
Development Tools
Jupyter Notebook
VS Code
Git
GitHub
⚙️ Installation
1. Clone the Repository
git clone https://github.com/poojakalloli/machine_learning_med_insurance.git
2. Navigate to the Project
cd machine_learning_med_insurance
3. Create Virtual Environment
python -m venv .venv
4. Activate Virtual Environment

Windows PowerShell:

.\.venv\Scripts\Activate.ps1
5. Install Dependencies
pip install -r requirements.txt
▶️ Run Streamlit Application
streamlit run Frontend/app_ui.py

Open:

http://localhost:8501
▶️ Run FastAPI Backend
uvicorn Backend.main:app --reload

Open:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
🧪 Example Prediction
Customer Information
Age       : 35
Sex       : Male
BMI       : 28.5
Children  : 0
Smoker    : Yes
Region    : Southeast
Prediction Result
Estimated Premium (INR)


₹1,583,353.52
Estimated Premium (USD)


$19,076.55

The prediction is generated using the trained Machine Learning pipeline.

📚 Key Machine Learning Concepts Demonstrated
Exploratory Data Analysis
Data Cleaning
Data Preprocessing
Feature Engineering
Categorical Encoding
Train-Test Split
Regression
Model Training
Model Comparison
Model Evaluation
MAE
MSE
RMSE
R² Score
Log Transformation
Inverse Transformation
Scikit-learn Pipeline
Joblib Model Serialization
FastAPI
Streamlit
Git
GitHub
Machine Learning Deployment
🔮 Future Improvements
SHAP-based model explainability
Feature importance visualization
Prediction confidence/range
Database-backed prediction history
User authentication
Advanced analytics dashboard
Automated model retraining
Model monitoring
Cloud API deployment
⚠️ Disclaimer

This application is developed for educational and demonstration purposes.

The predicted insurance premium is an ML-based estimate and should not be considered an actual insurance quote, financial advice, or medical advice.

👩‍💻 Author
Pooja Kalloli

Aspiring Data Scientist | Python | Machine Learning | Generative AI

GitHub:

https://github.com/poojakalloli

⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.



**That's the complete README.** You don't need to add anything else to it right now.
