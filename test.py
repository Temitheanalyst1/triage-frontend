# test.py
from triage import compute_triage

tests = [
    {
        "name": "Sickle cell crisis",
        "age": 24,
        "vitals": {"hr": 110, "rr": 20, "sbp": 110, "sat": 95, "temp_c": 37.0, "gcs": 15},
        "symptoms": {"pain_level": 9},
        "complaint_text": "sickle cell crisis with severe pain",
        "known_conditions": ["sickle_cell"]
    },
    {
        "name": "Chest pain + breathless",
        "age": 56,
        "vitals": {"hr": 120, "rr": 28, "sbp": 130, "sat": 92, "temp_c": 36.8, "gcs": 15},
        "symptoms": {"chest_pain": True, "breathlessness": True, "pain_level": 6},
        "complaint_text": "sudden chest pain and sweating",
        "known_conditions": []
    },
    {
        "name": "Mild headache",
        "age": 30,
        "vitals": {"hr": 78, "rr": 16, "sbp": 120, "sat": 98, "temp_c": 36.5, "gcs": 15},
        "symptoms": {"pain_level": 3},
        "complaint_text": "mild headache",
        "known_conditions": []
    },
    {
        "name": "Child breathing difficulty",
        "age": 2,
        "vitals": {"hr": 150, "rr": 40, "sbp": 90, "sat": 89, "temp_c": 38.0, "gcs": 15},
        "symptoms": {"breathlessness": True, "pain_level": 5},
        "complaint_text": "child severe cough and difficulty breathing",
        "known_conditions": []
    }
]

for p in tests:
    res = compute_triage(p)
    print("----")
    print(f"Patient: {p['name']} (age {p['age']})")
    print(f"Category: {res['category']}")
    print(f"Score: {res['score']}")
    print(f"Reason: {res['reason']}")
