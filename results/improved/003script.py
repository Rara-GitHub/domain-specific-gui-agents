import json
import os
from datetime import datetime

# Get current timestamp
current_time = datetime.now().isoformat()
encounter_date = "2025-01-09"

# Extract patient information from S002
patient_data = {
    "patient_id": "P002_JohnsonMichael",
    "demographics": {
        "full_name": {
            "last": "Johnson",
            "first": "Michael",
            "middle_initial": ""
        },
        "mrn": "P002",
        "date_of_birth": "",  # Not specified
        "age_range": "40-45 years",
        "gender": "Male",
        "contact_information": {
            "phone": "",
            "email": "",
            "address": ""
        },
        "marital_status": "Married",  # Wife mentioned
        "metadata": {
            "created_by": "HIMS_System",
            "created_at": current_time,
            "last_modified": current_time,
            "version": "1.0"
        }
    },
    "medical_history": {
        "bmi_category": "Obesity",
        "previous_visits": "Has visited GP in the past but no testing done previously",
        "surgeries": [],
        "chronic_conditions": [],
        "allergies": [],
        "current_medications": [],
        "social_history": {
            "smoking_status": "To be assessed",
            "alcohol_consumption": "To be assessed",
            "occupation": "To be determined",
            "living_situation": "Lives with wife"
        },
        "metadata": {
            "created_by": "HIMS_System",
            "created_at": current_time,
            "last_modified": current_time,
            "version": "1.0"
        }
    },
    "encounter": {
        "encounter_id": f"ENC_{encounter_date}_001",
        "date": encounter_date,
        "type": "General Practice Visit",
        "provider": "General Practitioner",
        "chief_complaint": "Sleeping problems and snoring",
        "history_of_present_illness": {
            "primary_symptoms": [
                {
                    "symptom": "Snoring",
                    "onset": "To be determined",
                    "duration": "Ongoing",
                    "severity": "Significant (wife complaining)",
                    "location": "N/A",
                    "quality": "Loud, disruptive",
                    "aggravating_factors": ["Alcohol", "Fatigue", "Sleeping position"],
                    "relieving_factors": ["Exercise"]
                },
                {
                    "symptom": "Sleep disturbance",
                    "onset": "Recent",
                    "duration": "Ongoing",
                    "severity": "Moderate to severe",
                    "associated_symptoms": ["Daytime sleepiness", "Possible gasping for air at night"]
                }
            ]
        },
        "review_of_systems": {
            "constitutional": ["Tiredness", "Daytime sleepiness", "Recent weight gain"],
            "respiratory": ["Possible sleep apnea episodes"],
            "cardiovascular": [],
            "neurological": ["Sleep pattern disruption"],
            "positive_findings": [
                "Snoring",
                "Daytime sleepiness",
                "Sleep disruption",
                "Obesity"
            ],
            "negative_findings": []
        },
        "physical_examination": {
            "vital_signs": {
                "bmi": "In obesity category"
            },
            "findings": []
        },
        "assessment": {
            "provisional_diagnosis": [
                {
                    "condition": "Obstructive Sleep Apnea",
                    "icd10_code": "G47.33",
                    "certainty": "Suspected",
                    "notes": "Based on snoring, daytime sleepiness, and obesity"
                }
            ],
            "differential_diagnosis": [
                {
                    "condition": "Insomnia",
                    "icd10_code": "G47.00",
                    "notes": "Less likely given patient falls asleep easily"
                }
            ]
        },
        "plan": {
            "immediate_interventions": [],
            "diagnostic_tests": [
                {
                    "test": "Sleep Study (Polysomnography)",
                    "type": "Neurological",
                    "urgency": "Urgent",
                    "reason": "To measure brain activity and oxygen levels during sleep",
                    "expected_timeframe": "4-6 weeks"
                }
            ],
            "referrals": [
                {
                    "specialty": "Sleep Medicine/Neurology",
                    "urgency": "Urgent",
                    "reason": "Suspected obstructive sleep apnea",
                    "expected_wait": "4-6 weeks"
                }
            ],
            "medications": [],
            "lifestyle_modifications": [
                "Weight loss if overweight",
                "Regular exercise",
                "Reduce stimulants (coffee, alcohol) especially before bedtime",
                "Maintain regular sleep schedule",
                "Caution with driving until diagnosis confirmed"
            ],
            "potential_treatments": [
                {
                    "treatment": "CPAP (Continuous Positive Airway Pressure)",
                    "type": "Medical Device",
                    "description": "Mask-like device worn during sleep to keep airway open",
                    "timing": "If diagnosis confirmed"
                }
            ],
            "follow_up": {
                "timeframe": "To be scheduled after sleep study results",
                "purpose": "Review sleep study results and discuss ongoing management"
            },
            "patient_education": [
                "Explained obstructive sleep apnea condition",
                "Discussed how airway muscles relax during sleep",
                "Warned about increased risk of heart conditions if untreated",
                "Advised about DVLA notification if diagnosis confirmed",
                "Suggested earplugs for spouse as temporary measure"
            ]
        },
        "metadata": {
            "created_by": "HIMS_System",
            "created_at": current_time,
            "last_modified": current_time,
            "version": "1.0",
            "data_quality_flags": [
                "Patient age is approximate (40-45 years)",
                "BMI exact value not specified",
                "Some patient responses not recorded in transcript",
                "Occupation to be determined (important for driving safety assessment)"
            ]
        }
    }
}

print("Extracted patient data for S002:")
print(json.dumps(patient_data, indent=2))
