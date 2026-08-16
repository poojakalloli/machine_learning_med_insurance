import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from io import BytesIO


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Medical Insurance Predictor",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# CUSTOM CSS — PROFESSIONAL THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- Color palette ---------- */
    :root {
        --brand-navy: #0f2a4a;
        --brand-blue: #1b4f8c;
        --brand-teal: #0e9488;
        --brand-teal-light: #14b8a6;
        --brand-bg: #f4f7fb;
        --brand-card: #ffffff;
        --brand-border: #e2e8f0;
        --brand-text: #1e293b;
        --brand-muted: #64748b;
        --brand-danger: #b91c1c;
        --brand-warning: #b45309;
        --brand-success: #047857;
    }

    /* ---------- App background ---------- */
    .stApp {
        background: linear-gradient(180deg, #f4f7fb 0%, #eef2f9 100%);
    }

    /* ---------- Header banner ---------- */
    .app-header {
        background: linear-gradient(120deg, var(--brand-navy) 0%, var(--brand-blue) 55%, var(--brand-teal) 100%);
        padding: 34px 40px;
        border-radius: 16px;
        margin-bottom: 28px;
        box-shadow: 0 10px 30px rgba(15, 42, 74, 0.25);
    }

    .main-title {
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 6px;
        color: #ffffff;
        letter-spacing: -0.5px;
    }

    .subtitle {
        font-size: 15px;
        color: rgba(255, 255, 255, 0.85);
        margin-bottom: 0;
        font-weight: 400;
    }

    /* ---------- Section headers ---------- */
    h2, h3 {
        color: var(--brand-navy) !important;
        font-weight: 700 !important;
    }

    /* ---------- Cards / containers ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--brand-card);
        border: 1px solid var(--brand-border) !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
        transition: box-shadow 0.2s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.10);
    }

    /* ---------- Profile labels/values ---------- */
    .profile-label {
        font-size: 11px;
        font-weight: 700;
        color: var(--brand-muted);
        letter-spacing: 0.8px;
        margin-bottom: 4px;
        text-transform: uppercase;
    }

    .profile-value {
        font-size: 19px;
        font-weight: 700;
        color: var(--brand-navy);
    }

    .profile-subtitle {
        font-size: 12px;
        color: var(--brand-teal);
        font-weight: 600;
    }

    /* ---------- Premium display ---------- */
    .premium-label {
        font-size: 12px;
        font-weight: 700;
        color: var(--brand-muted);
        letter-spacing: 0.6px;
        text-transform: uppercase;
    }

    .premium-value {
        font-size: 30px;
        font-weight: 800;
        color: var(--brand-teal);
        margin-top: 2px;
    }

    /* ---------- Buttons ---------- */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(120deg, var(--brand-blue), var(--brand-teal));
        color: #ffffff;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        padding: 0.6em 1.2em;
        box-shadow: 0 2px 8px rgba(27, 79, 140, 0.25);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton > button:hover, .stFormSubmitButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(27, 79, 140, 0.35);
    }

    .stDownloadButton > button {
        background: var(--brand-navy);
        color: #ffffff;
        border-radius: 8px;
        font-weight: 700;
        border: none;
    }

    /* ---------- Sliders / inputs accent ---------- */
    .stSlider [data-baseweb="slider"] > div > div {
        background: var(--brand-teal) !important;
    }

    /* ---------- Divider ---------- */
    hr {
        border-top: 1px solid var(--brand-border);
    }

    /* ---------- Alerts (info/success/warning) keep readable but tinted ---------- */
    div[data-testid="stAlert"] {
        border-radius: 10px !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="app-header">'
    '<div class="main-title">🏥 Medical Insurance Charge Predictor</div>'
    '<div class="subtitle">Predict estimated medical insurance charges using Machine Learning.</div>'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INITIALIZE SESSION STATE
# ============================================================

if "prediction_history" not in st.session_state:

    st.session_state["prediction_history"] = []


# ============================================================
# FUNCTIONS
# ============================================================

def get_bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


def get_prediction(payload):

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=payload,
        timeout=10
    )

    if response.status_code == 200:

        return response.json()

    raise Exception(
        f"Backend Error {response.status_code}: "
        f"{response.text}"
    )


def add_to_history(
    age,
    sex,
    bmi,
    children,
    smoker,
    region,
    premium_inr,
    premium_usd,
    prediction_type="Prediction"
):

    record = {
        "Time": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),

        "Type": prediction_type,

        "Age": age,

        "Sex": sex.title(),

        "BMI": round(bmi, 1),

        "BMI Category": get_bmi_category(bmi),

        "Children": children,

        "Smoker": smoker.title(),

        "Region": region.title(),

        "Premium (INR)": round(
            premium_inr,
            2
        ),

        "Premium (USD)": round(
            premium_usd,
            2
        )
    }

    st.session_state["prediction_history"].append(
        record
    )


# ============================================================
# CUSTOMER INFORMATION
# ============================================================

st.subheader("📝 Customer Information")

with st.form("insurance_form"):

    input_col1, input_col2 = st.columns(2)

    # --------------------------------------------------------
    # LEFT
    # --------------------------------------------------------

    with input_col1:

        age = st.slider(
            "Age",
            min_value=18,
            max_value=100,
            value=35
        )

        sex = st.selectbox(
            "Sex",
            ["male", "female"]
        )

        bmi = st.number_input(
            "BMI",
            min_value=10.0,
            max_value=60.0,
            value=28.5,
            step=0.1
        )

    # --------------------------------------------------------
    # RIGHT
    # --------------------------------------------------------

    with input_col2:

        children = st.selectbox(
            "Number of Children",
            [0, 1, 2, 3, 4, 5]
        )

        smoker = st.selectbox(
            "Smoker Status",
            ["yes", "no"]
        )

        region = st.selectbox(
            "Region",
            [
                "southeast",
                "southwest",
                "northwest",
                "northeast"
            ]
        )

    # --------------------------------------------------------
    # BMI
    # --------------------------------------------------------

    bmi_category = get_bmi_category(bmi)

    st.info(
        f"📊 BMI: **{bmi:.1f}** | "
        f"Category: **{bmi_category}**"
    )

    submit_btn = st.form_submit_button(
        "🔮 Calculate Premium"
    )


# ============================================================
# MAIN PREDICTION
# ============================================================

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

        # ----------------------------------------------------
        # API
        # ----------------------------------------------------

        data = get_prediction(payload)

        inr_val = data["predicted_inr"]

        usd_val = data["predicted_usd"]

        # ----------------------------------------------------
        # SESSION STATE
        # ----------------------------------------------------

        st.session_state["current_prediction"] = data

        st.session_state["current_age"] = age

        st.session_state["current_sex"] = sex

        st.session_state["current_bmi"] = bmi

        st.session_state["current_children"] = children

        st.session_state["current_smoker"] = smoker

        st.session_state["current_region"] = region

        # ----------------------------------------------------
        # ADD TO HISTORY
        # ----------------------------------------------------

        add_to_history(
            age=age,
            sex=sex,
            bmi=bmi,
            children=children,
            smoker=smoker,
            region=region,
            premium_inr=inr_val,
            premium_usd=usd_val,
            prediction_type="Prediction"
        )

        # ====================================================
        # PREMIUM RESULT
        # ====================================================

        st.markdown("---")

        st.subheader(
            "💰 Estimated Insurance Premium"
        )

        premium_col1, premium_col2 = st.columns(2)

        with premium_col1:

            with st.container(border=True):

                st.markdown(
                    '<div class="premium-label">'
                    'ESTIMATED PREMIUM (INR)'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="premium-value">'
                    f'₹{inr_val:,.2f}'
                    f'</div>',
                    unsafe_allow_html=True
                )

        with premium_col2:

            with st.container(border=True):

                st.markdown(
                    '<div class="premium-label">'
                    'ESTIMATED PREMIUM (USD)'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="premium-value">'
                    f'${usd_val:,.2f}'
                    f'</div>',
                    unsafe_allow_html=True
                )

        # ====================================================
        # CUSTOMER PROFILE
        # ====================================================

        st.markdown("---")

        st.subheader(
            "👤 Customer Profile"
        )

        profile1, profile2, profile3, profile4 = (
            st.columns(4)
        )

        # AGE
        with profile1:

            with st.container(border=True):

                st.markdown(
                    '<div class="profile-label">'
                    'AGE'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="profile-value">'
                    f'{age} years'
                    f'</div>',
                    unsafe_allow_html=True
                )

        # BMI
        with profile2:

            with st.container(border=True):

                st.markdown(
                    '<div class="profile-label">'
                    'BMI'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="profile-value">'
                    f'{bmi:.1f}'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="profile-subtitle">'
                    f'{bmi_category}'
                    f'</div>',
                    unsafe_allow_html=True
                )

        # SMOKER
        with profile3:

            with st.container(border=True):

                st.markdown(
                    '<div class="profile-label">'
                    'SMOKER'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="profile-value">'
                    f'{smoker.title()}'
                    f'</div>',
                    unsafe_allow_html=True
                )

        # REGION
        with profile4:

            with st.container(border=True):

                st.markdown(
                    '<div class="profile-label">'
                    'REGION'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="profile-value">'
                    f'{region.title()}'
                    f'</div>',
                    unsafe_allow_html=True
                )

        st.caption(
            f"**Profile:** {sex.title()} • "
            f"{children} children • "
            f"BMI {bmi:.1f} • "
            f"{bmi_category}"
        )

        # ====================================================
        # SMOKER MESSAGE
        # ====================================================

        if smoker == "yes":

            st.warning(
                "🚬 Smoking status is associated with higher "
                "insurance charges in this dataset. "
                "The prediction is based on the trained ML model."
            )

        else:

            st.success(
                "✅ Non-smoker profile selected."
            )

        # ====================================================
        # SUMMARY
        # ====================================================

        st.subheader(
            "💡 Prediction Summary"
        )

        st.write(
            f"""
            For a **{age}-year-old {sex}** with a BMI of
            **{bmi:.1f} ({bmi_category})**, {children}
            child/children, smoker status **{smoker}**, and
            region **{region}**, the model estimates an annual
            insurance charge of approximately:
            """
        )

        st.success(
            f"₹{inr_val:,.2f} / ${usd_val:,.2f}"
        )

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to the FastAPI backend."
        )

        st.code(
            "uvicorn Backend.main:app --reload",
            language="powershell"
        )

    except requests.exceptions.Timeout:

        st.error(
            "⏳ Backend request timed out."
        )

    except Exception as e:

        st.error(
            f"❌ Prediction Error: {e}"
        )


# ============================================================
# PHASE 2 — WHAT-IF ANALYSIS
# ============================================================

if "current_prediction" in st.session_state:

    st.markdown("---")

    st.header(
        "🔄 What-If Analysis"
    )

    st.write(
        "Change customer details and compare the new "
        "estimated premium with the current prediction."
    )

    # ========================================================
    # CURRENT VALUES
    # ========================================================

    current_age = st.session_state[
        "current_age"
    ]

    current_sex = st.session_state[
        "current_sex"
    ]

    current_bmi = st.session_state[
        "current_bmi"
    ]

    current_children = st.session_state[
        "current_children"
    ]

    current_smoker = st.session_state[
        "current_smoker"
    ]

    current_region = st.session_state[
        "current_region"
    ]

    current_inr = st.session_state[
        "current_prediction"
    ]["predicted_inr"]

    current_usd = st.session_state[
        "current_prediction"
    ]["predicted_usd"]

    # ========================================================
    # WHAT-IF INPUTS
    # ========================================================

    st.subheader(
        "🎯 Change Customer Details"
    )

    whatif_col1, whatif_col2 = st.columns(2)

    with whatif_col1:

        whatif_age = st.slider(
            "What-If Age",
            min_value=18,
            max_value=100,
            value=current_age,
            key="whatif_age"
        )

        whatif_bmi = st.number_input(
            "What-If BMI",
            min_value=10.0,
            max_value=60.0,
            value=float(current_bmi),
            step=0.1,
            key="whatif_bmi"
        )

        whatif_children = st.selectbox(
            "What-If Number of Children",
            [0, 1, 2, 3, 4, 5],
            index=current_children,
            key="whatif_children"
        )

    with whatif_col2:

        whatif_smoker = st.selectbox(
            "What-If Smoker Status",
            ["yes", "no"],
            index=(
                0
                if current_smoker == "yes"
                else 1
            ),
            key="whatif_smoker"
        )

        region_options = [
            "southeast",
            "southwest",
            "northwest",
            "northeast"
        ]

        whatif_region = st.selectbox(
            "What-If Region",
            region_options,
            index=region_options.index(
                current_region
            ),
            key="whatif_region"
        )

    whatif_bmi_category = get_bmi_category(
        whatif_bmi
    )

    st.info(
        f"📊 What-If BMI: **{whatif_bmi:.1f}** | "
        f"Category: **{whatif_bmi_category}**"
    )

    # ========================================================
    # COMPARE
    # ========================================================

    compare_btn = st.button(
        "🔄 Compare Premium",
        key="compare_premium"
    )

    if compare_btn:

        whatif_payload = {

            "age": whatif_age,

            "sex": current_sex,

            "bmi": whatif_bmi,

            "children": whatif_children,

            "smoker": whatif_smoker,

            "region": whatif_region
        }

        try:

            whatif_data = get_prediction(
                whatif_payload
            )

            whatif_inr = whatif_data[
                "predicted_inr"
            ]

            whatif_usd = whatif_data[
                "predicted_usd"
            ]

            difference_inr = (
                whatif_inr - current_inr
            )

            difference_usd = (
                whatif_usd - current_usd
            )

            # =================================================
            # COMPARISON
            # =================================================

            st.markdown("---")

            st.subheader(
                "📈 What-If Comparison"
            )

            compare_col1, compare_col2 = (
                st.columns(2)
            )

            with compare_col1:

                with st.container(border=True):

                    st.markdown(
                        "**CURRENT PREMIUM**"
                    )

                    st.markdown(
                        f"### ₹{current_inr:,.2f}"
                    )

                    st.caption(
                        f"Smoker: "
                        f"{current_smoker.title()}"
                    )

            with compare_col2:

                with st.container(border=True):

                    st.markdown(
                        "**WHAT-IF PREMIUM**"
                    )

                    st.markdown(
                        f"### ₹{whatif_inr:,.2f}"
                    )

                    st.caption(
                        f"Smoker: "
                        f"{whatif_smoker.title()}"
                    )

            # =================================================
            # DIFFERENCE
            # =================================================

            st.subheader(
                "💰 Premium Difference"
            )

            if difference_inr < 0:

                st.success(
                    f"""
                    🎉 The what-if scenario reduces the
                    estimated premium by:

                    **₹{abs(difference_inr):,.2f}**

                    USD difference:

                    **${abs(difference_usd):,.2f}**
                    """
                )

            elif difference_inr > 0:

                st.warning(
                    f"""
                    ⚠️ The what-if scenario increases the
                    estimated premium by:

                    **₹{difference_inr:,.2f}**

                    USD difference:

                    **${difference_usd:,.2f}**
                    """
                )

            else:

                st.info(
                    "The estimated premium is unchanged."
                )

            # =================================================
            # CHANGES
            # =================================================

            st.subheader(
                "🔍 What Changed?"
            )

            changed_features = []

            if whatif_age != current_age:

                changed_features.append(
                    f"Age: {current_age} → {whatif_age}"
                )

            if whatif_bmi != current_bmi:

                changed_features.append(
                    f"BMI: {current_bmi:.1f} → "
                    f"{whatif_bmi:.1f}"
                )

            if whatif_children != current_children:

                changed_features.append(
                    f"Children: {current_children} → "
                    f"{whatif_children}"
                )

            if whatif_smoker != current_smoker:

                changed_features.append(
                    f"Smoker: {current_smoker.title()} → "
                    f"{whatif_smoker.title()}"
                )

            if whatif_region != current_region:

                changed_features.append(
                    f"Region: {current_region.title()} → "
                    f"{whatif_region.title()}"
                )

            if not changed_features:

                st.info(
                    "No customer details were changed."
                )

            else:

                for feature in changed_features:

                    st.write(
                        f"• {feature}"
                    )

            # -------------------------------------------------
            # SAVE WHAT-IF TO HISTORY
            # -------------------------------------------------

            if st.checkbox(
                "📜 Save this What-If result to history",
                key="save_whatif"
            ):

                if (
                    "last_saved_whatif"
                    not in st.session_state
                    or
                    st.session_state[
                        "last_saved_whatif"
                    ] != whatif_inr
                ):

                    add_to_history(
                        age=whatif_age,
                        sex=current_sex,
                        bmi=whatif_bmi,
                        children=whatif_children,
                        smoker=whatif_smoker,
                        region=whatif_region,
                        premium_inr=whatif_inr,
                        premium_usd=whatif_usd,
                        prediction_type="What-If"
                    )

                    st.session_state[
                        "last_saved_whatif"
                    ] = whatif_inr

                    st.success(
                        "✅ What-If result saved to history."
                    )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to FastAPI."
            )

        except requests.exceptions.Timeout:

            st.error(
                "⏳ What-if request timed out."
            )

        except Exception as e:

            st.error(
                f"❌ What-If Error: {e}"
            )


# ============================================================
# PHASE 3 — PROFESSIONAL PREDICTION HISTORY
# ============================================================

st.markdown("---")

st.header("📜 Prediction History")

history = st.session_state["prediction_history"]

# ============================================================
# NO HISTORY
# ============================================================

if len(history) == 0:

    st.info(
        "No prediction history yet. "
        "Make your first prediction to see it here."
    )

# ============================================================
# HISTORY AVAILABLE
# ============================================================

else:

    history_df = pd.DataFrame(history)

    total_predictions = len(history_df)

    latest_premium = history_df.iloc[-1]["Premium (INR)"]

    average_premium = history_df["Premium (INR)"].mean()

    overview1, overview2, overview3 = st.columns(3)

    with overview1:

        with st.container(border=True):

            st.caption("TOTAL PREDICTIONS")

            st.markdown(
                f"### {total_predictions}"
            )

    with overview2:

        with st.container(border=True):

            st.caption("LATEST PREMIUM")

            st.markdown(
                f"### ₹{latest_premium:,.0f}"
            )

    with overview3:

        with st.container(border=True):

            st.caption("AVERAGE PREMIUM")

            st.markdown(
                f"### ₹{average_premium:,.0f}"
            )

    st.markdown("")

    # ========================================================
    # RECENT PREDICTIONS
    # ========================================================

    st.subheader("🧾 Recent Predictions")

    for index, record in reversed(
        list(enumerate(history))
    ):

        prediction_number = index + 1

        with st.container(border=True):

            # HEADER
            header_col1, header_col2 = st.columns([4, 1])

            with header_col1:

                st.markdown(
                    f"**🕐 {record['Time']}**"
                )

            with header_col2:

                st.markdown(
                    f"**Prediction #{prediction_number}**"
                )

            # CUSTOMER PROFILE
            st.caption("👤 CUSTOMER PROFILE")

            profile1, profile2, profile3, profile4 = st.columns(4)

            with profile1:

                st.caption("AGE")

                st.markdown(
                    f"**{record['Age']} years**"
                )

            with profile2:

                st.caption("BMI")

                st.markdown(
                    f"**{record['BMI']:.1f}**"
                )

                st.caption(
                    record["BMI Category"]
                )

            with profile3:

                st.caption("SMOKER")

                st.markdown(
                    f"**{record['Smoker']}**"
                )

            with profile4:

                st.caption("REGION")

                st.markdown(
                    f"**{record['Region']}**"
                )

            # PROFILE SUMMARY
            st.caption(
                f"**Profile:** "
                f"{record['Sex']} • "
                f"{record['Children']} children • "
                f"BMI {record['BMI']:.1f} • "
                f"{record['BMI Category']}"
            )

            # PREMIUM
            premium1, premium2 = st.columns(2)

            with premium1:

                st.caption(
                    "💰 ESTIMATED PREMIUM (INR)"
                )

                st.markdown(
                    f"### ₹{record['Premium (INR)']:,.2f}"
                )

            with premium2:

                st.caption(
                    "ESTIMATED PREMIUM (USD)"
                )

                st.markdown(
                    f"### ${record['Premium (USD)']:,.2f}"
                )

    # ========================================================
    # EXPORT
    # ========================================================

    st.markdown("---")

    st.subheader("📥 Export History")

    export_col1, export_col2 = st.columns(2)

    with export_col1:

        csv_data = history_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Download Prediction History",
            data=csv_data,
            file_name="insurance_prediction_history.csv",
            mime="text/csv",
            use_container_width=True
        )

    with export_col2:

        if st.button(
            "🗑️ Clear Prediction History",
            use_container_width=True
        ):

            st.session_state["prediction_history"] = []

            st.success(
                "Prediction history cleared."
            )

            st.rerun()
