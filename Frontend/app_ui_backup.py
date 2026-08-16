import streamlit as st
import requests

# Page setup
st.set_page_config(page_title="Medical Insurance Predictor", page_icon="🏥", layout="centered")

# Visual Styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Medical Insurance Charge Predictor")
st.write("Streamlit Frontend communicating with FastAPI Machine Learning Backend.")

st.markdown("---")

# Input Form
with st.form("insurance_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.slider("Age", 18, 100, 35)
        sex = st.selectbox("Sex", ["male", "female"])
        bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=28.5, step=0.1)
        
    with col2:
        children = st.selectbox("Number of Children", [0, 1, 2, 3, 4, 5])
        smoker = st.selectbox("Smoker Status", ["yes", "no"])
        region = st.selectbox("Region", ["southeast", "southwest", "northwest", "northeast"])
        
    submit_btn = st.form_submit_button("Calculate Premium")

# Call FastAPI Endpoint on Form Submission
if submit_btn:
    payload = {
        "age": age,
        "sex": sex,
        "bmi": bmi,
        "children": children,
        "smoker": smoker,
        "region": region
    }
    
    try:
        # Send HTTP POST request to FastAPI backend
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            inr_val = data["predicted_inr"]
            usd_val = data["predicted_usd"]
            
            st.markdown("---")
            st.subheader("Results")
            
            res_col1, res_col2 = st.columns(2)
            res_col1.metric(label="Estimated Premium (INR)", value=f"₹{inr_val:,.2f}")
            res_col2.metric(label="Estimated Premium (USD)", value=f"${usd_val:,.2f}")
            
            if smoker == "yes":
                st.warning("⚠️ **Health Alert:** Smoking increases annual insurance charges by over 200%.")
        else:
            st.error("Error connecting to backend API.")
            
    except Exception as e:
        st.error(f"Failed to connect to backend server: {e}")