# triage.py

def triage_patient(age, gender, symptoms, pain_level, conditions):
    """
    A simple triage function that assigns a patient to Critical, Urgent, or General
    based on symptoms, age, pain, and existing conditions.
    """

    score = 0
    reason = []

    # --- Symptom-based scoring ---
    if "chest pain" in symptoms:
        score += 5
        reason.append("Chest pain")
    if "breathing" in " ".join(symptoms):
        score += 6
        reason.append("Difficulty breathing")
    if "fever" in symptoms:
        score += 1
        reason.append("Fever detected")
    if "sickle cell" in conditions:
        score += 4
        reason.append("Sickle cell crisis reported")

    # --- Pain level ---
    if pain_level >= 7:
        score += 2
        reason.append(f"High pain level {pain_level}/10")

    # --- Existing conditions ---
    if "hypertension" in conditions:
        score += 2
        reason.append("Hypertension history")
    if "diabetes" in conditions:
        score += 2
        reason.append("Diabetes history")

    # --- Age factors ---
    if age <= 5:
        score += 3
        reason.append("Child (age ≤5)")
    if age >= 70:
        score += 3
        reason.append("Elderly (age ≥70)")

    # --- Decide category ---
    if score >= 8:
        category = "Critical"
    elif score >= 4:
        category = "Urgent"
    else:
        category = "General"

    # ✅ FIX: Return as a dictionary, not a tuple
    return {
        "Category": category,
        "Score": score,
        "Reason": "; ".join(reason) if reason else "No urgent symptoms"
    }

