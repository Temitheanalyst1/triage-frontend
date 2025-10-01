
import streamlit as st
import random
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="Emergency Care Dashboard (Prototype)", layout="wide")

# ---------------------
# Utilities & Mock Data
# ---------------------

FIRST_NAMES = ["Alex","Sam","Jordan","Taylor","Riley","Morgan","Casey","Jamie","Avery","Cameron",
               "Lee","Robin","Neil","Ike","Noah","Maya","Zara","Lina","Ola","Ethan"]
LAST_NAMES = ["Adams","Bell","Clark","Davis","Evans","Ford","Green","Hall","Irwin","James",
              "Khan","Lopez","Miller","Nguyen","Osei","Patel","Quinn","Reed","Smith","Young"]

CRITICAL_SYMPTOMS = [
    "None", "Severe chest pain", "Difficulty breathing", "Stroke symptoms", "Loss of consciousness",
    "Uncontrolled bleeding", "Severe allergic reaction", "Severe burns", "Seizure",
    "Severe pain crisis", "Poisoning/overdose", "Severe head injury"
]
OTHER_SYMPTOMS = [
    "None", "Fever", "Headache", "Cough", "Sore throat", "Nausea", "Vomiting", "Diarrhea",
    "Abdominal pain", "Back pain", "Dizziness", "Fatigue", "Joint pain",
    "Mild breathing issues", "Minor cuts/bruises"
]
HIGH_RISK_CONDITIONS = [
    "None", "Diabetes","Heart disease","Asthma","COPD","Cancer","Kidney disease","Liver disease",
    "Pregnant","Immune compromised","Organ transplant","Blood disorders","Sickle cell disease","Hemophilia"
]
OTHER_CONDITIONS = [
    "None", "High blood pressure","Arthritis","Depression","Anxiety","Migraine","Allergies",
    "Thyroid disease","Osteoporosis"
]

def random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def assign_priority_from_data(patient):
    """Assigns priority level automatically"""
    # Filter out "None" from selections
    critical = [item for item in patient.get("critical", []) if item != "None"]
    high_risk = [item for item in patient.get("high_risk", []) if item != "None"]
    
    if critical:
        return "🚨 Life-threatening (Critical)", "red"
    if high_risk or patient.get("age", 0) <= 5 or patient.get("age", 0) >= 65:
        return "🟠 Vulnerable (High Priority)", "orange"
    return "🟢 Standard Care", "green"

def make_mock_patient(idx=None, force_priority=None):
    """Create one mock patient dict"""
    age = random.choice([random.randint(1,4), random.randint(5,15), random.randint(16,40),
                         random.randint(41,64), random.randint(65,90)])
    critical = []
    high_risk = []
    other_symptoms = []

    if force_priority == "critical" or random.random() < 0.12:
        critical = random.sample(CRITICAL_SYMPTOMS, k=1)
    if force_priority == "vulnerable" or random.random() < 0.2:
        high_risk = random.sample(HIGH_RISK_CONDITIONS, k=1)
    other_symptoms = random.sample(OTHER_SYMPTOMS, k=random.randint(0,2))

    patient = {
        "id": idx if idx is not None else random.randint(1000,9999),
        "name": random_name(),
        "age": age,
        "critical": critical,
        "other_symptoms": other_symptoms,
        "high_risk": high_risk,
        "other_conditions": random.sample(OTHER_CONDITIONS, k=random.randint(0,1)),
        "check_in": (datetime.now() - timedelta(minutes=random.randint(0,120))).isoformat(),
        "status": random.choices(["waiting","in_treatment"], weights=[0.6,0.4])[0]
    }
    patient["priority"], patient["color"] = assign_priority_from_data(patient)
    return patient

def get_treatment_duration(priority):
    """Get expected treatment duration based on priority"""
    if "Life-threatening" in priority:
        return 15
    elif "Vulnerable" in priority:
        return 25
    else:
        return 10

def calculate_wait_time(patient, queue_position):
    """Calculate estimated wait time for a patient"""
    priority_value = 1 if "Life-threatening" in patient["priority"] else (2 if "Vulnerable" in patient["priority"] else 3)
    
    # Count patients ahead with same or higher priority
    patients_ahead = 0
    for i, p in enumerate(st.session_state.queue_patients):
        if i >= queue_position:
            break
        p_priority = 1 if "Life-threatening" in p["priority"] else (2 if "Vulnerable" in p["priority"] else 3)
        if p_priority <= priority_value:
            patients_ahead += 1
    
    # Calculate wait time based on treatment durations
    wait_time = 0
    for i, p in enumerate(st.session_state.queue_patients):
        if i >= queue_position:
            break
        p_priority = 1 if "Life-threatening" in p["priority"] else (2 if "Vulnerable" in p["priority"] else 3)
        if p_priority <= priority_value:
            wait_time += get_treatment_duration(p["priority"])
    
    return wait_time

def get_waiting_minutes(check_in_time):
    """Calculate minutes since check-in"""
    check_in = datetime.fromisoformat(check_in_time)
    now = datetime.now()
    return int((now - check_in).total_seconds() / 60)

def initialize_sample_queue_data():
    """Initialize sample data for queue management"""
    if not st.session_state.queue_patients and not st.session_state.treatment_patients:
        # Sample waiting patients
        sample_waiting = [
            {
                "id": 1001,
                "name": "John Doe",
                "priority": "🚨 Life-threatening (Critical)",
                "check_in": (datetime.now() - timedelta(minutes=5)).isoformat(),
                "age": 45
            },
            {
                "id": 1002,
                "name": "Mary Smith", 
                "priority": "🟠 Vulnerable (High Priority)",
                "check_in": (datetime.now() - timedelta(minutes=10)).isoformat(),
                "age": 67
            },
            {
                "id": 1003,
                "name": "Alex Johnson",
                "priority": "🟢 Standard Care",
                "check_in": (datetime.now() - timedelta(minutes=3)).isoformat(),
                "age": 28
            },
            {
                "id": 1004,
                "name": "Fatima Ali",
                "priority": "🟠 Vulnerable (High Priority)", 
                "check_in": (datetime.now() - timedelta(minutes=7)).isoformat(),
                "age": 34
            }
        ]
        
        # Sample patients in treatment
        sample_treatment = [
            {
                "id": 2001,
                "name": "Peter Brown",
                "priority": "🚨 Life-threatening (Critical)",
                "treatment_start": (datetime.now() - timedelta(minutes=12)).isoformat(),
                "expected_duration": 15,
                "age": 52
            },
            {
                "id": 2002,
                "name": "Grace Kim",
                "priority": "🟢 Standard Care",
                "treatment_start": (datetime.now() - timedelta(minutes=5)).isoformat(),
                "expected_duration": 10,
                "age": 31
            },
            {
                "id": 2003,
                "name": "Ahmed Musa",
                "priority": "🟠 Vulnerable (High Priority)",
                "treatment_start": (datetime.now() - timedelta(minutes=18)).isoformat(),
                "expected_duration": 25,
                "age": 58
            }
        ]
        
        st.session_state.queue_patients = sample_waiting
        st.session_state.treatment_patients = sample_treatment

# --------------------------
# Initialize session storage
# --------------------------
if "patients" not in st.session_state:
    st.session_state.patients = []
    for i in range(18):
        if i < 3:
            p = make_mock_patient(idx=2000+i, force_priority="critical")
        elif i < 7:
            p = make_mock_patient(idx=2000+i, force_priority="vulnerable")
        else:
            p = make_mock_patient(idx=2000+i)
        st.session_state.patients.append(p)

if "current_patient_id" not in st.session_state:
    st.session_state.current_patient_id = None

if "checkin_completed" not in st.session_state:
    st.session_state.checkin_completed = False

if "form_selections" not in st.session_state:
    st.session_state.form_selections = {
        "critical": [],
        "other": [],
        "high_risk": [],
        "other_conditions": []
    }

# Initialize queue management data
if "queue_patients" not in st.session_state:
    st.session_state.queue_patients = []
if "treatment_patients" not in st.session_state:
    st.session_state.treatment_patients = []
if "completed_patients" not in st.session_state:
    st.session_state.completed_patients = []

if "show_queue_management" not in st.session_state:
    st.session_state.show_queue_management = False

# -------------------------
# Page 1: Check-in form (always visible)
# -------------------------
st.title("🏥 Emergency Care Dashboard (Prototype)")

# Show check-in form
st.subheader("📋 Medical Check-in Form")
st.write("**Required:** Please fill in your name, age, and select at least one option from any of the categories below to access the triage dashboard.")

with st.form("checkin_form", clear_on_submit=False):
    col1, col2 = st.columns([2,1])
    with col1:
        full_name = st.text_input("Full Name", placeholder="Enter patient's full name")
    with col2:
        age = st.number_input("Age", min_value=0, max_value=120, value=30, step=1)

    with st.expander("🔴 Critical Emergency Symptoms"):
        selected_critical = st.multiselect("", CRITICAL_SYMPTOMS, default=st.session_state.form_selections["critical"], key="critical_symptoms")
    with st.expander("🟡 Other Current Symptoms"):
        selected_other = st.multiselect("", OTHER_SYMPTOMS, default=st.session_state.form_selections["other"], key="other_symptoms")
    with st.expander("🟠 High-Risk Medical Conditions"):
        selected_high_risk = st.multiselect("", HIGH_RISK_CONDITIONS, default=st.session_state.form_selections["high_risk"], key="high_risk_conditions")
    with st.expander("⚪ Other Medical Conditions"):
        selected_other_conditions = st.multiselect("", OTHER_CONDITIONS, default=st.session_state.form_selections["other_conditions"], key="other_conditions")

    submitted = st.form_submit_button("✅ Complete Medical Check-in")

# Handle "None" selections - make them mutually exclusive
def handle_none_selections(selected_list):
    """Handle None selections to be mutually exclusive"""
    if "None" in selected_list and len(selected_list) > 1:
        # If None is selected with other options, keep only None
        return ["None"]
    return selected_list

# Apply None handling to all selections and update session state
selected_critical = handle_none_selections(selected_critical)
selected_other = handle_none_selections(selected_other)
selected_high_risk = handle_none_selections(selected_high_risk)
selected_other_conditions = handle_none_selections(selected_other_conditions)

# Update session state
st.session_state.form_selections = {
    "critical": selected_critical,
    "other": selected_other,
    "high_risk": selected_high_risk,
    "other_conditions": selected_other_conditions
}

# Handle form submission
if submitted:
    # Validate all required fields
    errors = []
    
    if not full_name.strip():
        errors.append("Please enter a name.")
    
    if age <= 0:
        errors.append("Please enter a valid age.")
    
    # Check if all categories are set to "None" or empty
    all_none_or_empty = (
        (not selected_critical or selected_critical == ["None"]) and
        (not selected_other or selected_other == ["None"]) and
        (not selected_high_risk or selected_high_risk == ["None"]) and
        (not selected_other_conditions or selected_other_conditions == ["None"])
    )
    
    if all_none_or_empty:
        errors.append("Please select at least one medical symptom or condition from any category to proceed.")
    
    if errors:
        for error in errors:
            st.error(error)
    else:
        new_patient = {
            "id": random.randint(10000,99999),
            "name": full_name.strip(),
            "age": age,
            "critical": selected_critical,
            "other_symptoms": selected_other,
            "high_risk": selected_high_risk,
            "other_conditions": selected_other_conditions,
            "check_in": datetime.now().isoformat(),
            "status": "waiting"
        }
        new_patient["priority"], new_patient["color"] = assign_priority_from_data(new_patient)
        st.session_state.patients.append(new_patient)
        st.session_state.current_patient_id = new_patient["id"]
        st.session_state.checkin_completed = True
        st.success("✅ Check-in completed successfully! The dashboard is now available below.")
        st.rerun()

# -------------------------
# Page 2: Dashboard + Queue (only visible after check-in)
# -------------------------
if st.session_state.checkin_completed:
    # Create smooth transition effect using Streamlit
    if "dashboard_loaded" not in st.session_state:
        st.session_state.dashboard_loaded = True
        
        # Create loading animation
        loading_placeholder = st.empty()
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate loading with progress
        for i in range(101):
            progress_bar.progress(i)
            if i < 30:
                status_text.text("🔄 Loading dashboard...")
            elif i < 60:
                status_text.text("📊 Processing patient data...")
            elif i < 90:
                status_text.text("🎯 Calculating priorities...")
            else:
                status_text.text("✅ Dashboard ready!")
            time.sleep(0.02)  # Small delay for smooth effect
        
        # Clear loading elements
        loading_placeholder.empty()
        progress_bar.empty()
        status_text.empty()
    
    st.markdown("---")
    st.header("🩺 Triage Dashboard")
    st.write("Welcome to the emergency care dashboard. Your information has been added to the queue.")

    patients = st.session_state.patients
    total_patients = len(patients)
    waiting_count = sum(1 for p in patients if p["status"] == "waiting")
    in_treatment_count = sum(1 for p in patients if p["status"] == "in_treatment")
    crit_count = sum(1 for p in patients if "Life-threatening" in p["priority"])
    vul_count = sum(1 for p in patients if "Vulnerable" in p["priority"])
    gen_count = sum(1 for p in patients if "Standard Care" in p["priority"])

    def pct(n): return (n / total_patients * 100) if total_patients else 0

    # Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("👥 Total Patients", total_patients)
    c2.metric("⏳ Waiting", waiting_count)
    c3.metric("🩺 In Treatment", in_treatment_count)

    st.markdown("### 🚨 Priority Breakdown")
    c1, c2, c3 = st.columns(3)
    c1.metric("🔴 Life-threatening", crit_count, f"{pct(crit_count):.1f}%")
    c2.metric("🟠 Vulnerable", vul_count, f"{pct(vul_count):.1f}%")
    c3.metric("🟢 General", gen_count, f"{pct(gen_count):.1f}%")

    # Ordered waiting queue
    def priority_value(p):
        if "Life-threatening" in p["priority"]: return 1
        if "Vulnerable" in p["priority"]: return 2
        return 3

    waiting_patients = sorted(
        [p for p in patients if p["status"] == "waiting"],
        key=lambda x: (priority_value(x), x["check_in"])
    )

    st.subheader("⏭️ Next Up (Top 3)")
    for idx, p in enumerate(waiting_patients[:3], start=1):
        st.markdown(f"**#{idx} — {p['name']}** • {p['priority']} • Age: {p['age']}")

    st.subheader("👥 Full Waiting Queue")
    for pos, p in enumerate(waiting_patients, start=1):
        marker = " **(YOU)** " if p["id"] == st.session_state.current_patient_id else ""
        st.markdown(f"**{pos}. {p['name']}**{marker} — {p['priority']} — Age: {p['age']}")

    # Show current patient status
    if st.session_state.current_patient_id:
        cp = next((x for x in patients if x["id"] == st.session_state.current_patient_id), None)
        if cp and cp["status"] == "waiting":
            pos = waiting_patients.index(cp) + 1
            st.info(f"📌 You are **#{pos}** in the queue. {pos-1} ahead of you.")
        elif cp:
            st.info("✅ You are currently in treatment.")

    # Action buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚨 View Emergency Queue Management", type="primary"):
            st.session_state.show_queue_management = True
            st.rerun()
    
    with col2:
        if st.button("🔄 Start New Check-in"):
            st.session_state.checkin_completed = False
            st.session_state.current_patient_id = None
            st.session_state.dashboard_loaded = False  # Reset loading state
            st.session_state.show_queue_management = False  # Hide queue management
            st.session_state.form_selections = {
                "critical": [],
                "other": [],
                "high_risk": [],
                "other_conditions": []
            }
            st.rerun()

else:
    # Show message when dashboard is not available
    st.markdown("---")
    st.info("👆 Complete the medical check-in form above to access the triage dashboard.")

# -------------------------
# Page 3: Emergency Queue Management (only visible when accessed from dashboard)
# -------------------------
if st.session_state.show_queue_management:
    st.markdown("---")
    st.header("🚨 Emergency Queue Management")
    
    # Back to dashboard button
    if st.button("← Back to Dashboard"):
        st.session_state.show_queue_management = False
        st.rerun()

    # Initialize sample data
    initialize_sample_queue_data()

    # Auto-refresh every 30 seconds
    if st.button("🔄 Refresh Queue Status"):
        st.rerun()

    # Add new patient from check-in to queue
    if st.session_state.checkin_completed and st.session_state.current_patient_id:
        # Check if current patient is already in queue
        current_patient_in_queue = any(p["id"] == st.session_state.current_patient_id for p in st.session_state.queue_patients)
        if not current_patient_in_queue:
            # Find the patient in the main patients list
            current_patient = next((p for p in st.session_state.patients if p["id"] == st.session_state.current_patient_id), None)
            if current_patient:
                # Add to queue
                queue_patient = {
                    "id": current_patient["id"],
                    "name": current_patient["name"],
                    "priority": current_patient["priority"],
                    "check_in": current_patient["check_in"],
                    "age": current_patient["age"]
                }
                st.session_state.queue_patients.append(queue_patient)

    # Sort queue by priority
    def priority_sort_key(patient):
        if "Life-threatening" in patient["priority"]:
            return (1, patient["check_in"])  # Critical first, then by check-in time
        elif "Vulnerable" in patient["priority"]:
            return (2, patient["check_in"])  # Vulnerable second, then by check-in time
        else:
            return (3, patient["check_in"])  # General last, then by check-in time

    st.session_state.queue_patients.sort(key=priority_sort_key)

    # Section 1: Waiting Queue
    st.subheader("⏳ Waiting Queue")
    if st.session_state.queue_patients:
        for i, patient in enumerate(st.session_state.queue_patients):
            waited_mins = get_waiting_minutes(patient["check_in"])
            est_remaining = calculate_wait_time(patient, i)
            expected_wait = get_treatment_duration(patient["priority"])
            
            # Check if patient is overdue
            is_overdue = waited_mins > expected_wait
            
            col1, col2, col3, col4, col5, col6 = st.columns([2, 1.5, 1, 1.5, 1, 1])
            
            with col1:
                if is_overdue:
                    st.markdown(f"**🔴 {patient['name']}** (ID: {patient['id']})")
                else:
                    st.markdown(f"**{patient['name']}** (ID: {patient['id']})")
            
            with col2:
                st.write(patient["priority"])
            
            with col3:
                if is_overdue:
                    st.markdown(f"<span style='color: red; font-weight: bold;'>{waited_mins} mins</span>", unsafe_allow_html=True)
                else:
                    st.write(f"{waited_mins} mins")
            
            with col4:
                st.write(f"{est_remaining} mins")
            
            with col5:
                if is_overdue:
                    st.markdown("<span style='color: red; font-weight: bold;'>OVERDUE</span>", unsafe_allow_html=True)
                else:
                    st.write("Waiting")
            
            with col6:
                col6a, col6b = st.columns(2)
                with col6a:
                    if st.button("✅", key=f"complete_queue_{patient['id']}", help="Mark as Complete"):
                        # Move to completed
                        st.session_state.completed_patients.append(patient)
                        st.session_state.queue_patients.remove(patient)
                        st.rerun()
                with col6b:
                    if st.button("⏳", key=f"waiting_queue_{patient['id']}", help="Still Waiting"):
                        st.info(f"{patient['name']} is still waiting")
    else:
        st.info("No patients currently waiting in queue.")

    # Section 2: Patients in Treatment
    st.subheader("🩺 Patients in Treatment")
    if st.session_state.treatment_patients:
        for patient in st.session_state.treatment_patients:
            treatment_mins = get_waiting_minutes(patient["treatment_start"])
            expected_duration = patient["expected_duration"]
            is_overdue = treatment_mins > expected_duration
            
            col1, col2, col3, col4, col5, col6 = st.columns([2, 1.5, 1, 1, 1, 1])
            
            with col1:
                if is_overdue:
                    st.markdown(f"**🔴 {patient['name']}** (ID: {patient['id']})")
                else:
                    st.markdown(f"**{patient['name']}** (ID: {patient['id']})")
            
            with col2:
                st.write(patient["priority"])
            
            with col3:
                st.write(f"{expected_duration} mins")
            
            with col4:
                if is_overdue:
                    st.markdown(f"<span style='color: red; font-weight: bold;'>{treatment_mins} mins</span>", unsafe_allow_html=True)
                else:
                    st.write(f"{treatment_mins} mins")
            
            with col5:
                if is_overdue:
                    st.markdown("<span style='color: red; font-weight: bold;'>OVERDUE</span>", unsafe_allow_html=True)
                else:
                    st.write("In Treatment")
            
            with col6:
                if st.button("✅", key=f"complete_treatment_{patient['id']}", help="Mark as Complete"):
                    # Move to completed
                    st.session_state.completed_patients.append(patient)
                    st.session_state.treatment_patients.remove(patient)
                    st.rerun()
    else:
        st.info("No patients currently in treatment.")

    # Section 3: Move next patient from queue to treatment
    if st.session_state.queue_patients:
        st.subheader("🔄 Queue Management")
        next_patient = st.session_state.queue_patients[0]
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**Next patient:** {next_patient['name']} ({next_patient['priority']})")
        with col2:
            if st.button("🚀 Start Treatment", key="start_treatment"):
                # Move from queue to treatment
                treatment_patient = {
                    "id": next_patient["id"],
                    "name": next_patient["name"],
                    "priority": next_patient["priority"],
                    "treatment_start": datetime.now().isoformat(),
                    "expected_duration": get_treatment_duration(next_patient["priority"]),
                    "age": next_patient["age"]
                }
                st.session_state.treatment_patients.append(treatment_patient)
                st.session_state.queue_patients.remove(next_patient)
                st.rerun()

    # Section 4: Statistics
    st.subheader("📊 Queue Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Waiting", len(st.session_state.queue_patients))
    col2.metric("In Treatment", len(st.session_state.treatment_patients))
    col3.metric("Completed Today", len(st.session_state.completed_patients))
    col4.metric("Total Active", len(st.session_state.queue_patients) + len(st.session_state.treatment_patients))

    # Section 5: Treatment Duration Guidelines
    with st.expander("ℹ️ Treatment Duration Guidelines"):
        st.markdown("""
        **Default Estimated Treatment Durations:**
        - 🔴 **Critical (Life-threatening)**: ~15 minutes
        - 🟠 **Vulnerable (High Priority)**: ~25 minutes  
        - 🟢 **General (Standard Care)**: ~10 minutes
        
        **Queue Priority Order:**
        1. Critical patients first
        2. Vulnerable patients second
        3. General patients last
        
        **Overdue Indicators:**
        - Waiting time exceeds expected treatment duration
        - Treatment time exceeds expected duration
        - Highlighted in red for immediate attention
        """)