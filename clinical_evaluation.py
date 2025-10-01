import streamlit as st

st.set_page_config(page_title="Clinical Evaluation", layout="wide")

st.title("🩺 Clinical Evaluation")
st.subheader("Detailed patient assessment for priority care")

# Patient vitals
st.markdown("### Patient Vitals")
col1, col2, col3, col4 = st.columns(4)

with col1:
    heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, step=1)
with col2:
    blood_pressure_systolic = st.number_input("Systolic BP (mmHg)", min_value=50, max_value=250, step=1)
with col3:
    blood_pressure_diastolic = st.number_input("Diastolic BP (mmHg)", min_value=30, max_value=150, step=1)
with col4:
    temperature = st.number_input("Temperature (°C)", min_value=30.0, max_value=45.0, step=0.1)

# Oxygen saturation
oxygen = st.number_input("Oxygen Saturation (%)", min_value=50, max_value=100, step=1)

# Pain assessment
pain_level = st.slider("Pain Level (0 = no pain, 10 = worst pain)", 0, 10, 0)

# Mental Status / Consciousness
mental_status = st.selectbox(
    "Mental Status",
    ["Alert", "Drowsy", "Confused", "Unresponsive"]
)

# Additional Risk Factors
st.markdown("### Additional Risk Factors")
risk_factors = st.multiselect(
    "Select any additional risk factors",
    ["Recent surgery", "Infection", "Pregnancy", "Immunocompromised", "Chronic disease"]
)

# Submit and scoring
if st.button("✅ Complete Clinical Evaluation"):
    st.success("Evaluation completed!")
    
    # Simple scoring example based on vitals & risk factors
    score = 0
    if heart_rate < 50 or heart_rate > 120:
        score += 2
    if blood_pressure_systolic < 90 or blood_pressure_systolic > 180:
        score += 2
    if oxygen < 94:
        score += 3
    if pain_level >= 7:
        score += 1
    if mental_status != "Alert":
        score += 3
    score += len(risk_factors)

    # Determine patient priority (without saying "triage")
    if score >= 7:
        priority = "🚨 High Priority"
    elif score >= 4:
        priority = "🟠 Medium Priority"
    else:
        priority = "🟢 Low Priority"

    st.write("**Patient Score:**", score)
    st.write("**Priority Level:**", priority)
    st.write("**Selected Risk Factors:**", risk_factors)
